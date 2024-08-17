import cv2
import easyocr
import matplotlib.pyplot as plt

import os
from gtts import gTTS
import playsound

import time

def speak(text):
    if os.path.exists('voice.mp3'): #delete file if it alredy exists so its blank
        os.remove('voice.mp3')
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


 

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



