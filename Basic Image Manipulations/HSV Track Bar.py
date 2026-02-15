import cv2
import numpy as np

img = cv2.imread('../Images/Shapes With Color.png', 1)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
def call_back(x):
    pass
cv2.namedWindow('HSV Track Bar')
cv2.resizeWindow('HSV Track Bar', 400, 225)
cv2.createTrackbar('Hue Min', 'HSV Track Bar', 0, 179, call_back)
cv2.createTrackbar('Hue Max', 'HSV Track Bar', 179, 179, call_back)
cv2.createTrackbar('Satur Min', 'HSV Track Bar', 0, 255, call_back)
cv2.createTrackbar('Satur Max', 'HSV Track Bar', 255, 255, call_back)
cv2.createTrackbar('Value Min', 'HSV Track Bar', 0, 255, call_back)
cv2.createTrackbar('Value Max', 'HSV Track Bar', 255, 255, call_back)

"""
Hàm call_back được gọi một cách tự động trong trường hợp sau :
Nó được gọi mỗi khi bạn tác động vào thanh Trackbar.
Cụ thể là :
Khi bạn dùng chuột kéo thanh trượt: Mỗi pixel bạn dịch chuyển, hàm sẽ được gọi liên tục.
Khi bạn click chuột vào một vị trí bất kỳ trên thanh trượt : Hàm sẽ được gọi một lần để 
cập nhật giá trị tại vị trí đó.
Ngay khi chương trình vừa chạy (tùy phiên bản) : Đôi khi OpenCV sẽ gọi nó một lần đầu 
tiên để khởi tạo giá trị mặc định.
"""

while True:
    h_min = cv2.getTrackbarPos('Hue Min', 'HSV Track Bar')
    h_max = cv2.getTrackbarPos('Hue Max', 'HSV Track Bar')
    s_min = cv2.getTrackbarPos('Satur Min', 'HSV Track Bar')
    s_max = cv2.getTrackbarPos('Satur Max', 'HSV Track Bar')
    v_min = cv2.getTrackbarPos('Value Min', 'HSV Track Bar')
    v_max = cv2.getTrackbarPos('Value Max', 'HSV Track Bar')
    lower_value = np.array([h_min, s_min, v_min])
    upper_value = np.array([h_max, s_max, v_max])
    img_result = cv2.inRange(img_hsv, lower_value, upper_value)
    contours, hierarchy = cv2.findContours(img_result, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Số lượng contours : {len(contours)}")
    img_draw = img.copy() # tạo ra 1 tấm ảnh gốc mới rồi cho vẽ lên đó
    for contour in contours:
        cv2.drawContours(img_draw, contour, -1, (0, 255, 0), 3)
    cv2.imshow('Result', img_result)
    cv2.imshow('Original', img_draw)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()
