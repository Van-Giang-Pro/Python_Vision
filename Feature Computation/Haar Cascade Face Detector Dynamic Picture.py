import cv2
import cv2.data
import numpy as np

#Load file cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#Kiểm tra file cascade có được load thành công hay không
if face_cascade.empty():
    print("Không tìm thấy file cascade")
    exit()
else:
    print("File cascade đã được load thành công")
#Tạo hàm để đọc hình ảnh truyền từ webcam
def detect_faces_realtime():
    #Khởi tạo webcam
    cap = cv2.VideoCapture(0) # 0 là webcam mặc định
    #Kiểm tra xem camera có hoạt động được hay không
    if not cap.isOpened():
        print("Không thể mở camera")
        return
    while True:
        #Đọc frame từ camera
        ret, frame = cap.read()
        #Kiểm tra xem frame có đươc đọc thành công hay chưa
        if not ret:
            print("Không thể đọc frame")
            break
        #Chuyển frame sang ảnh xám
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #Nhận diện khuôn mặt
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=3, minSize=(100,100))
        #Vẽ hình chữ nhật lên ảnh phát hiện khuôn mặt
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #Thêm text hiển thị "Face" vào ảnh
            cv2.putText(frame, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0, 0), 2)
        #Hiển thị số khuôn mặt được phát hiện được
        cv2.putText(frame, f"Faces: {len(faces)}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        #Hiển thị frame
        cv2.imshow("Face Detection", frame)
        #Nhấn bất kỳ phím nào để thoái
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #Giải phóng camera và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    #Gọi hàm detect_faces_realtime để chạy chương trình
    detect_faces_realtime()

