import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox

#setting up camera, index will let you pick through a few 
video = cv2.VideoCapture(1)

while True:
    ret, frame = video.read()

    cv2.imshow("Object Detection", frame)

    if cv2.waitKey(1) & 0xFF ==  ord("q"):
        break