import cv2
import easyocr
import matplotlib.pyplot as plt

from pygame import mixer 
import pyttsx3
import time
import wave

#install pyttsx3, opencv-contrib-python, cvlib, pygame, matplotlib, easyocr,  PyObjC


#init and setup TTS libraries
mixer.init() 
speaker = pyttsx3.init()
speaker.setProperty('rate', 150)  # Speed of speech (words per minute)
speaker.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)

#helper function for TTS
def get_duration_wave(file_path):
   with wave.open(file_path, 'r') as audio_file:
      frame_rate = audio_file.getframerate()
      n_frames = audio_file.getnframes()
      duration = n_frames / float(frame_rate)
      return duration

#TTS generation function
def speak(text):
    speaker.save_to_file(text, "output.wav")
    speaker.runAndWait()
    mixer.music.load("output.wav") 
    
#testing tts
# note the pygame command is nonobstructing so there must be code to continously run the program for the audio to run  
speak("hello this is a test")
mixer.music.play() 
time.sleep(get_duration_wave("output.wav"))



#read image 
image_path = 'C:/Users/Harsh/OneDrive/Documents/Projects/Hackathon/Ignition Hacks/ReadAble/Images/test3.jpg'

img = cv2.imread(image_path)

#instance text detector

# reader = easyocr.Reader(["en"], gpu=False)

# text_ = reader.readtext(img)

# myBook = 'This is an example of a story where aryaen refuses to cooperate'

# for t in text_:
#     bbox, text, score = t
#     print(text)

# plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
# plt.show()



