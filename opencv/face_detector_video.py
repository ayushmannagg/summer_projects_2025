import cv2
cap = cv2.VideoCapture(0)

face_detect = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

while True:
    isTrue, frame = cap.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.flip(gray_frame,1)
    roi = face_detect.detectMultiScale(gray_frame, 1.2,3)
    print(roi)

    for x,y,w,h in roi:
        cv2.rectangle(gray_frame, (x,y), (x+h, y+w), (255,0,45), 3)

    cv2.putText(gray_frame,f"Number of Person: {len(roi)}", (50,50), 2, 1, (20,240,90), 3)

    cv2.imshow("Read Faces", gray_frame)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break