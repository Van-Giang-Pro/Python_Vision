import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap, QImage
import cv2

base_dir = os.path.join(os.path.dirname(__file__), 'Webcam Trigger App.ui')
# Ta có __file__ là một biến đặc biệt trong Python, nó chứa đường dẫn tuyệt đối đến tệp Python hiện tại đang được thực thi.

class App(QMainWindow): # Đây không phải là 1 tòa nhà thật sự, đây chỉ là một bản thiết kế
    def __init__(self):
        super().__init__() # Là dòng lệnh bắt buộc phải có ở đầu hàm khởi tạo của một lớp con.
        # Nó đảm bảo rằng tất cả các công việc thiết lập cần thiết của lớp cha được thực hiện trước khi lớp con bắt đầu thực hiện các công việc riêng của mình.
        loadUi(base_dir, self)
        self.btn_trigger.setText("Trigger")
        # self.btn_trigger.clicked.connect(self.trigger_image)
        self.btn_trigger.clicked.connect(self.trigger_webcam)
        # Khởi tạo webcam
        self.cap = cv2.VideoCapture(0) # Ta có self là để tham chiếu đến chính bản thân đối tượng
        if self.cap.isOpened():
            print("Webcam Opened Successfully")
        else:
            print("Failed To Open Webcam")

    def trigger_image(self): # Vì bên trong method, bạn có thể cần truy cập các thuộc tính hoặc method khác của đối tượng.
        # Vì trigger_camera là một method nằm bên trong class App, nên nó thuộc về đối tượng
        self.lb_image.setPixmap(QPixmap(os.path.join(os.path.dirname(__file__), '..', 'Images', 'Fanuc.png')))
        # Dấu '..' là lùi lại 1 thư mục

    def trigger_webcam(self):
        if not self.cap.isOpened():
            print("Webcam Not Opened")
            return
        ret, frame = self.cap.read()
        if ret:
            # Chuyển BGR (OpenCV) sang RGB (Qt)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w # Mỗi pixel có 3 kênh tương ứng với mỗi kênh 1 byte
            q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888) # Ba số 8 là byte per channel
            # Hiển thị lên QLabel
            pixmap = QPixmap.fromImage(q_image) # Convert ảnh thành pixmap
            self.lb_image.setPixmap(pixmap.scaled(self.lb_image.width(), self.lb_image.height())) # Tạo ra một bản sao của pixmap với kích thước phù hợp với QLabel
            print("Webcam Triggered Successfully")
        else:
            print("Failed To Read Frame")

if __name__ == '__main__':
    app = QApplication(sys.argv) # Chính là thành phố, là nền tảng, môi trường hoạt động của toàn bộ ứng dụng
    # Ta có sys.argv là một danh sách chứa các đối số được truyền vào chương trình khi nó được chạy
    mainWindow = App() # Chính là toà nhà trong thành phố
    mainWindow.show()
    sys.exit(app.exec()) # Đảm bảo rằng chường trình sẽ thoát sạch khi người dùng đóng cửa sổ
