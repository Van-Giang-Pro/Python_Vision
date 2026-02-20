import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtGui import QPixmap

class App(QMainWindow): # Đây không phải là 1 tòa nhà thật sự, đây chỉ là một bản thiết kế
    def __init__(self):
        super().__init__() # Là dòng lệnh bắt buộc phải có ở đầu hàm khởi tạo của một lớp con.
        # Nó đảm bảo rằng tất cả các công việc thiết lập cần thiết của lớp cha được thực hiện trước khi lớp con bắt đầu thực hiện các công việc riêng của mình.
        loadUi(r'C:\Users\fs120806\Desktop\Document\Programing Project\Python_Vision\App\Basler Camera Trigger App UI.ui', self)
        self.btn_trigger.setText("Trigger")
        self.btn_trigger.clicked.connect(self.trigger_camera)
        # Vì trigger_camera là một method nằm bên trong class App, nên nó thuộc về đối tượng
        self.lb_image.setPixmap(QPixmap(r'C:\Users\fs120806\Desktop\Document\Programing Project\Python_Vision\Images\Fanuc.png'))
    def trigger_camera(self): # Vì bên trong method, bạn có thể cần truy cập các thuộc tính hoặc method khác của đối tượng.
        print("Camera Triggered")

if __name__ == '__main__':
    app = QApplication(sys.argv) # Chính là thành phố, là nền tảng, môi trường hoạt động của toàn bộ ứng dụng
    # Ta có sys.argv là một danh sách chứa các đối số được truyền vào chương trình khi nó được chạy
    mainWindow = App() # Chính là toà nhà trong thành phố
    mainWindow.show()
    sys.exit(app.exec_()) # Đảm bảo rằng chường trình sẽ thoát sạch khi người dùng đóng cửa sổ
