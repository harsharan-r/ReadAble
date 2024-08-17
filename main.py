import cv2
import easyocr
import matplotlib.pyplot as plt

#read image 
image_path = 'C:/Users/Harsh/OneDrive/Documents/Projects/Hackathon/Ignition Hacks/ReadAble/Images/test.png'

img = cv2.imread(image_path)

#instance text detector

reader = easyocr.Reader(["en"], gpu=False)

text_ = reader.readtext(img)

myBook = ''

for t in text_:
    bbox, text, score = t

    cv2.rectangle(img, bbox[0], bbox[2], (0,255,0), 5)

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()



