import re

import cv2
import numpy as np
import pytesseract as ptr

ptr.pytesseract.tesseract_cmd = r'C:\Users\fs120806\AppData\Local\Programs\Tesseract OCR\tesseract.exe'
img = cv2.imread("../Images/License Plate 1.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gaussian_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
edged = cv2.Canny(gaussian_blur, 75, 200)
# Ta có 2 thông số cuối cùng là ngưỡng dưới và ngưỡng trên
# kernel = np.ones((6,6), np.uint8)
# closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 2))
dilated = cv2.dilate(edged, kernel, iterations=1)
contours, hierachy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
rect_roi = None
for contour in contours:
    approx_contour = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
    x, y, w, h = cv2.boundingRect(approx_contour) # Nhận vào 1 contour và trả về thông số hình chữ nhật
    area  = w * h
    ratio = w / h if h !=0 else 0
    if 30000 < area < 50000 and 1.0 < ratio < 9.0:
        rect_roi = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_gray = img_gray[y:y+h, x:x+w]
if rect_roi is not None:
    retval, rect_roi_bin = cv2.threshold(roi_gray, 127, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    config = "--oem 3 --psm 7"
    license_plate_text = ptr.image_to_string(rect_roi_bin, config=config)
    license_plate_text = re.sub(r'[^A-Za-z0-9]', '', license_plate_text)
    print(f"Biển số xe : {license_plate_text}")
cv2.imshow("Image", img)
# cv2.imshow("Gray", img_gray)
# cv2.imshow("Gaussian Blur", gaussian_blur)
cv2.imshow("Canny Edged", edged)
cv2.imshow("Closed", dilated)

cv2.waitKey(0)
cv2.destroyAllWindows()
