import cv2
import cv2.data
import numpy as np

#Load file cascade
eyes_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")
#Kiểm tra file cascade có được load thành công hay không
if eyes_cascade.empty():
    print("Không tìm thấy file cascade")
    exit()
else:
    print("File cascade đã được load thành công")
#Tạo hàm để đọc hình ảnh truyền từ webcam
def detect_eyes_realtime():
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
        eyes = eyes_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=3, minSize=(24,24))
        #Vẽ hình chữ nhật lên ảnh phát hiện mắt
        for (x, y, w, h) in eyes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            #Thêm text hiển thị "Face" vào ảnh
            cv2.putText(frame, "Eyes", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0, 0), 2)
        #Hiển thị số mắt được phát hiện được
        cv2.putText(frame, f"Eyes: {len(eyes)}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        #Hiển thị frame
        cv2.imshow("Eyes Detection", frame)
        #Nhấn bất kỳ phím nào để thoái
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    #Giải phóng camera và đóng cửa sổ
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    #Gọi hàm detect_faces_realtime để chạy chương trình
    detect_eyes_realtime()

