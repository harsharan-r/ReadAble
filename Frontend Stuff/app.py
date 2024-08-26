from flask import Flask, Response, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, emit
import os
import cv2
from PyMultiDictionary import MultiDictionary
import time

import mediapipe as mp
import easyocr
import threading

import main

dictionary = MultiDictionary()
app = Flask(__name__)
socketio = SocketIO(app)

# Setting up the camera
video = cv2.VideoCapture(1)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

hands = mphands.Hands()

release = True
interrupt = False
finished = True

wordsDictionary = {}

definedWord = "easy"
prevDefinedWord = ""

image_width = 640
image_height = 480

book_text = ""

image_path = 'C:/Users/Harsh/OneDrive/Documents/Projects/Hackathon/Ignition Hacks/ReadAble/Images/test3.jpg'
ocr_frame = cv2.imread(image_path)
bbtop = [0,0]
bbbot = [0,0]

def get_definition(word): #function to get the defenition of supplied variable
    word=str(word)
    defenitionstring=str((dictionary.meaning('en',word)))
    defenitionlist=defenitionstring.split("]")
    defenitionlist.remove(defenitionlist[0])
    defenitionstring=str(defenitionlist[0])
    defenitionlist=defenitionstring.split("\'")   
        
    if str(defenitionlist[1])=='':
        return "Unknown Word"
    else:
        return defenitionlist[1]


# Simulate variable changes in Python and emit updated definitions
def simulate_variable_change():
    global finished
    socketio.emit('update_definition', {'word': definedWord, 'definition': get_definition(definedWord)})
    time.sleep(0.3)
    finished = True

def readFrame(img):
    global main,wordsDictionary,book_text,playback_speed
    main.wpm = 150 * playback_speed
    reader = easyocr.Reader(["en"], gpu=False)
    text = ""
    bboxs = []
    delays = []
    
    for t in reader.readtext(img):
        bbox, text_, score = t
        bboxs.append(bbox)
        text += (" " + text_)
    
        wordsDictionary[text_] = [tuple(map(int, bbox[0])), tuple(map(int, bbox[2]))]
        delays.append((len(text_.split())/main.wpm*60))

    book_text = text

    main.speak(text)
    main.mixer.music.play()
    highlightWords(bboxs, delays)

def Pause():
    main.mixer.music.pause()

def Resume():
    main.mixer.music.unpause()
    

def highlightWords(bboxs, delays):
    
    global bbtop, bbbot
    for i,bbox in enumerate(bboxs):
        # Draw a bounding box around the recognized text area
        bbtop = tuple(map(int, bbox[0]))
        bbbot = tuple(map(int, bbox[2]))
        
        # Delay to simulate the reading pace
        while interrupt:
            time.sleep(0.5)
        time.sleep(delays[i])
        

    bbtop = [0,0]
    bbbot = [0,0]
        
        # Optional: You can clear the previous bounding box by drawing over it with the original frame, 
        # or simply keep adding bounding boxes as the reading progresses.
    
def loop():
    global release,interrupt,definedWord,finished, prevDefinedWord
    while True:
        success, frame = video.read()
        
        # if not ret:
        #     return

        frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mphands.HAND_CONNECTIONS)
                fingerx = hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP].x * image_width
                fingery = hand_landmarks.landmark[mphands.HandLandmark.INDEX_FINGER_TIP].y * image_height


            if len(list(wordsDictionary.values()))>0:
                closest = 1000
                closest_index = 0

                for i,pos in enumerate(list(wordsDictionary.values())):
                    if abs(fingery - pos[1][1]) < closest:
                        closest = abs(fingery-pos[1][1])
                        closest_index = i

            
                closest_xvalue = list(wordsDictionary.values())[closest_index][0][0]
                closest_string = list(wordsDictionary.keys())[closest_index]
                intervals = abs(closest_xvalue - list(wordsDictionary.values())[closest_index][1][0])/len(closest_string.split())

                posx = closest_xvalue
                closest = 1000
                closest_index = 0

                for i in range(len(closest_string.split())):
                    if abs(fingerx - posx) < closest:
                        closest = abs(fingerx - posx)
                        closest_index = i
                    posx += intervals

                definedWord = closest_string.split()[closest_index]
                
                
                # Define the text to display
                text = definedWord

                if finished and prevDefinedWord != definedWord:
                    socketio.start_background_task(simulate_variable_change)
                    finished = False
                    prevDefinedWord = definedWord

                # Set the position, font, scale, color, and thickness
                position = (50, 50)
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 1
                color = (0, 255, 0)  # Green color in BGR
                thickness = 2

                # Add text to the frame
                cv2.putText(frame, text, position, font, font_scale, color, thickness)
    

            if main.mixer.music.get_busy():
                Pause()
                interrupt = True

        else:
            if interrupt:
                Resume()
                interrupt = False

            elif release:
                # Run readFrame in a separate thread
                thread = threading.Thread(target=readFrame, args=(frame,))
                thread.start()
                release = False


        cv2.rectangle(frame, bbtop, bbbot, (0, 255, 0), 2)

        # Encode frame as JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield the frame in byte format
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    

#------------------------------------------------------------------------------------------------------------
            
folder_dir = os.path.join(os.getcwd(), "book storage")      

playback_speed = 1.0

@app.route('/toggle_speed', methods=['POST'])
def toggle_speed():
    global playback_speed
    playback_speed = 2.0 if playback_speed == 1.0 else 1.0
    print(playback_speed)
    return jsonify({'status': 'success', 'new_speed': playback_speed})

@app.route('/save_words', methods=['POST'])
def save_words():

    filename = request.form['bookname']

    # Sanitize the filename to avoid issues
    sanitized_filename = "".join(c for c in filename if c.isalnum() or c in (" ", "_", "-")).rstrip()

    # Simulate recognized words (replace with your ML model output)
    recognized_words = book_text

    # Save to a new file in the books directory
    filepath = os.path.join(folder_dir, f"{sanitized_filename}.txt")
    with open(filepath, 'a') as f:
        f.write(recognized_words + "\n")

    return redirect(url_for('camera_page'))

# Route to display the saved books
@app.route('/display_books')
def display_books():
    # Get a list of all text files in the books directory
    all_files = os.listdir(folder_dir)
    # Remove the .txt extension from each filename
    files = [os.path.splitext(f)[0] for f in all_files if f.endswith('.txt')]
    # Read the contents of the file
    return render_template('books.html', files=files)

@app.route('/book_content/<filename>')
def book_content(filename):
    # Ensure the filename has .txt extension
    file_path = os.path.join(folder_dir, filename + '.txt')
    # Read the contents of the file
    with open(file_path, 'r') as file:
        content = file.read()
    return jsonify({"content": content})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera')
def camera_page():
    return render_template('camera.html')

@app.route('/books')
def books():
    # Get a list of all text files in the books directory
    all_files = os.listdir(folder_dir)
    # Remove the .txt extension from each filename
    files = [os.path.splitext(f)[0] for f in all_files if f.endswith('.txt')]
    return render_template('books.html', files=files)

@app.route('/video_feed')
def video_feed():
    return Response(loop(), mimetype='multipart/x-mixed-replace; boundary=frame')
        
@app.route('/set_boolean', methods=['POST'])
def set_boolean():
    global release
    data = request.get_json()
    release = data.get('boolean_value', False)
    print(release)
    return jsonify({'status': 'success', 'new_value': release})


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5001)
    # Start the background task that simulates variable changes

    
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)

video.release()
cv2.destroyAllWindows()