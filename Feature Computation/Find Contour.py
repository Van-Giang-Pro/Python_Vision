import cv2

img = cv2.imread('../Images/Hex Nut.png')
img_resize = cv2.resize(img, (400, 400))
img_gray = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (7, 7), 0)
ret, img_binary = cv2.threshold(img_blur, 90, 255, cv2.THRESH_BINARY_INV)
# Ta có cv2.RETR_TREE là lấy tất cả các đường bao và thiết lập một gia phả
# Ta có cv2.RETR_EXTERNAL là lấy đường bao ngoài cùng
contours, hierarchy = cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# Giá trị contour này sẽ trả về python list
# Hàm findcontour nó coi màu trắng là vật thể màu đen là nền
# Ta có cv2.CHAIN_APPROX_SIMPLE là loại bỏ các điểm thừa chỉ lấy điểm đầu và cuối
# Thay vì lấy hàng trăm điểm ở giữa
print(f"Số lượng đường biên tìm thấy được : {len(contours)}")
print("Contours : ", contours)
cv2.drawContours(img_resize, contours, -1, (0, 255, 0), 3)
# Ta có -1 là vẽ hết tất cả các đường bao tìm thấy
cv2.putText(img_resize, f"Quantity : {len(contours)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
# Ta có cv2.LINE_AA quy định nét vẽ của chữ, mịn hay không mịn
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    area = cv2.contourArea(contour)
    print(f"Diện tích : {area}")
    cv2.rectangle(img_resize, (x, y), (x + w, y + h), (0, 0, 255), 2)
cv2.imshow('Contours', img_resize)
# cv2.imshow('Blur', img_blur)
# cv2.imshow('Gray', img_gray)
# cv2.imshow('Binary', img_binary)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
Trong OpenCV, khi hàm cv2.findContours tìm các đường viền, nó có một quy ước rất thông minh :
Đường viền bao ngoài (Outer Contour) : các điểm của đường viền bao quanh một vật thể sẽ được
sắp xếp theo chiều ngược chiều kim đồng hồ (CCW).
Đường viền của lỗ bên trong (Inner Contour) : các điểm của đường viền tạo thành một cái lỗ
bên trong một vật thể sẽ được sắp xếp theo chiều cùng chiều kim đồng hồ (CW).
Giá trị dương : thường xảy ra khi đường bao được vẽ theo chiều ngược chiều kim đồng hồ.
Giá trị âm : thường xảy ra khi đường bao được vẽ theo chiều cùng chiều kim đồng hồ.
"""