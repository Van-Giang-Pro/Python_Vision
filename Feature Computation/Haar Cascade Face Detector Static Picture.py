import cv2
import cv2.data
import numpy as np

# Đọc ảnh
img = cv2.imread('../Images/Friends.jpeg')
#Kiểm tra ảnh đã được đọc thành công hay chưa
if  img is None:
    print("Không tìm thấy ảnh")
    exit()
else:
    print("Ảnh đã được đọc thành công")
# Hiển thị ảnh
cv2.imshow('Friends', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
#Chuyển ảnh sang ảnh xám
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#Hiển thị ảnh xám 
cv2.imshow("Friends_Gray", img_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
#Tạo file cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#Kiểm tra
if face_cascade.empty():
    print("Không tìm thấy file cascade")
    exit()
else:
    print("File cascade đã được load thành công")
#Nhận dạng khuôn mặt
faces = face_cascade.detectMultiScale(
    img_gray,
    scaleFactor=3,
    minNeighbors=5,
    minSize=(10,10)
)
#Vẽ hình chữ nhật
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
#Hiển thị ảnh
cv2.imshow("Friends_Face", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

