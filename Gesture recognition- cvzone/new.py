import cv2
import time
import numpy as np
import cvzone.HandTrackingModule as htm
wCam, hCam = 640, 480



cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.HandDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    
    cTime  =time.time()
    fps = 1/(cTime-pTime)
    pTime=cTime

    cv2.putText(img, f'FPS: {int (fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0), 3)
    hands,img = detector.findHands(img)#with draw
    hands,img = detector.findHands(img, draw = False) #no draw
    if hands:
        lmList = hands[0]
        fingerUp=detector.fingersUp(lmList)
        if len(lmList) !=0:
            print(lmList)


    cv2.imshow("Image", img)
    cv2.waitKey(1)



