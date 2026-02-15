import cv2
import numpy as np

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
while True:
    ret, frame = cap.read()
    if ret == False:
        print("Frame capture failed")
        break
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_value = np.array([30, 0, 0])
    upper_value = np.array([50, 255, 255])
    img_mask = cv2.inRange(frame_hsv, lower_value, upper_value)
    contours, hierarchy = cv2.findContours(img_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 6000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, "Yellow", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break
cv2.destroyAllWindows()
