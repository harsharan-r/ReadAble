import cv2
import mediapipe as mp
import easyocr
import threading
import time

# Setting up the camera
video = cv2.VideoCapture(1)

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mphands = mp.solutions.hands

hands = mphands.Hands()

release = True

# Assuming these are functions and attributes in the 'main' module
import main  

image_path = 'C:/Users/Harsh/OneDrive/Documents/Projects/Hackathon/Ignition Hacks/ReadAble/Images/test3.jpg'
ocr_frame = cv2.imread(image_path)
bbtop = [0,0]
bbbot = [0,0]

def readFrame(img):
    global main
    reader = easyocr.Reader(["en"], gpu=False)
    text = ""
    bboxs = []
    
    for t in reader.readtext(img):
        bbox, text_, score = t
        bboxs.append(bbox)
        text += (" " + text_)
    
    main.speak(text)
    main.mixer.music.play()
    highlightWords(bboxs, len(text), main.wpm)
    

def highlightWords(bboxs, words, wpm):
    delay = words / wpm
    global bbtop, bbbot
    print(bboxs)

    for bbox in bboxs:
        # Draw a bounding box around the recognized text area
        bbtop = tuple(map(int, bbox[0]))
        bbbot = tuple(map(int, bbox[2]))
        
        print(bbbot)

        # Delay to simulate the reading pace
        time.sleep(delay)
        
        # Optional: You can clear the previous bounding box by drawing over it with the original frame, 
        # or simply keep adding bounding boxes as the reading progresses.
    
def loop():
    global release
    ret, frame = video.read()
    
    if not ret:
        return

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mphands.HAND_CONNECTIONS)
    else:
        if release:
            # Run readFrame in a separate thread
            thread = threading.Thread(target=readFrame, args=(frame,))
            thread.start()
            release = False


    cv2.rectangle(frame, bbtop, bbbot, (0, 255, 0), 2)
    cv2.imshow("Object Detection", frame)

while True:
    loop()

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the video capture object and close all OpenCV windows
video.release()
cv2.destroyAllWindows()
