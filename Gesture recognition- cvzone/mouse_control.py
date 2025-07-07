import cv2
import mediapipe as mp
import pyautogui as pyg
import time
import numpy as np
x1 = y1 = x2 = y2 = 0

mp_hands = mp.solutions.hands.Hands()
mp_drawing = mp.solutions.drawing_utils
my_hands = mp.solutions.hands
screen_width, screen_height = pyg.size()
cap = cv2.VideoCapture(0)
a = False
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame,1)
    if not ret:
        break

    frame_height, frame_width, depth = frame.shape
    
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = mp_hands.process(rgb_image)
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            mp_drawing.draw_landmarks(frame, hand)
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                if id == 8:                    
                    cv2.circle(img = frame, center = (x,y), radius = 8, color = (0,255,255), thickness = 3)
                    x1 = x
                    y1 = y
                if id == 4:
                    cv2.circle(img = frame, center = (x,y), radius = 8, color = (0,0,255), thickness = 3)
                    x2 = x
                    y2 = y
                cx, cy = (x1+x2)//2, (y1 + y2)//2
                index_finger_y = hand.landmark[my_hands.HandLandmark.INDEX_FINGER_TIP].y
                middle_finger_y = hand.landmark[my_hands.HandLandmark.MIDDLE_FINGER_TIP].y
                ring_finger_y = hand.landmark[my_hands.HandLandmark.RING_FINGER_TIP].y
                pinky_y = hand.landmark[my_hands.HandLandmark.PINKY_TIP].y
                thumb_y = hand.landmark[my_hands.HandLandmark.THUMB_TIP].y
        

        dist = ((x2-x1)**2 + (y2-y1)**2)**(0.5)//4
        cv2.line(frame, (x1,y1), (x2,y2),(255,255,0), 5)
        cv2.circle(frame,(cx,cy), 8, (0,255,0),3 )
        if (thumb_y<index_finger_y and thumb_y<middle_finger_y and thumb_y<ring_finger_y and thumb_y<pinky_y):
            a = True
        if a == True:
            mouse_x = (screen_width/frame_width * x)
            mouse_y = (screen_height/frame_height * y)
            if (dist < 7):
                pyg.click()
            pyg.moveTo(mouse_x,mouse_y)
        # if dist>20:
        #     pyg.press("volumeup", presses = 1)
        # else:
        #     pyg.press("volumedown", presses = 1)
        # print(dist)


    cv2.imshow("Hand Gesture", frame)
    # cv2.imshow('MediaPipe Hands', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()