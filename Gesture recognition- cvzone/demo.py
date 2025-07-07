import cv2
import mediapipe as mp
import pyautogui as pyg
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7) as hands:

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip the image for a later selfie-view display
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        
                index_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
                thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                x = index_finger_y - thumb_y

                print ("index", index_finger_y)
                print("thumb", thumb_y)
                # cv2.line(frame, (index_finger_x, index_finger_y), (thumb_x, thumb_y), (255,0,255), 3 )





                if index_finger_y < thumb_y:
                    hand_gesture = "pointing up"
                elif index_finger_y > thumb_y:
                    hand_gesture = "pointing down"
                else:
                    hand_gesture = "other"

                if hand_gesture == "pointing up":
                    pyg.press("volumeup")
                elif hand_gesture == "pointing down":
                    pyg.press("volumedown")
        cv2.imshow("Hand Gesture", frame)

        
        # cv2.imshow('MediaPipe Hands', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()