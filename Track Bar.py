import cv2

from pygments.formatters import img
img = cv2.imread("Images/Friends.jpeg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Hiển thị cửa sổ
# Ta có Window Normal cho phép cửa sổ được điều chỉnh kích thước
cv2.namedWindow("Track Bar", cv2.WINDOW_NORMAL)
def call_back(x):
    pass
cv2.createTrackbar("Threshold", "Track Bar", 100, 255, call_back)
# Mặc định của trackbar min là 0 còn nếu tạo trackbar min thì giới hạn được min là bao nhiêu
cv2.setTrackbarMin("Threshold", "Track Bar", 0)
while True:
    value = cv2.getTrackbarPos("Threshold", "Track Bar")
    print(f"Giá trị hiện tại của trackbar : {value}")
    retval, img_binary = cv2.threshold(img_gray, value, 255, cv2.THRESH_BINARY)
    # Ta có retval trả về giá trị ngưỡng được sử dụng trong quá trình phân đoạn ảnh
    # Nếu dùng phân ngưỡng Otsu thì giá trị trả về là ngưỡng tìm được
    cv2.imshow("Original Image", img)
    cv2.imshow("Binary Image", img_binary)
    cv2.waitKey(1) # Nếu không có waitkey thì chương trình sẽ chạy liên tục và bị lỗi
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cv2.destroyAllWindows()