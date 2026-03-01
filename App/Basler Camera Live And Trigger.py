import sys, os
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.uic import loadUi
from PyQt6.QtGui import QPixmap, QImage
import cv2
from pyorbbecsdk import *
from pyorbbecsdk import OBSensorType, VideoStreamProfile, OBFormat, OBError, FrameSet
from utils import frame_to_bgr_image

base_dir = os.path.join(os.path.dirname(__file__), 'Trigger And Live App.ui')
# Ta có __file__ là một biến đặc biệt trong Python, nó chứa đường dẫn tuyệt đối đến tệp Python hiện tại đang được thực thi.

class App(QMainWindow): # Đây không phải là 1 tòa nhà thật sự, đây chỉ là một bản thiết kế
    def __init__(self):
        super().__init__() # Là dòng lệnh bắt buộc phải có ở đầu hàm khởi tạo của một lớp con.
        # Nó đảm bảo rằng tất cả các công việc thiết lập cần thiết của lớp cha được thực hiện trước khi lớp con bắt đầu thực hiện các công việc riêng của mình.
        loadUi(base_dir, self)
        self.pipeline = Pipeline() # Động cơ kết nối camera, theo cấu hình pipeline, nếu không có self thì chỉ dùng trong hàm init thôi
        self.config = Config() # Bản thiết kế lưu cấu hình, độ phân giải, fps và format, nếu không có self thì chỉ dùng trong hàm init thôi
        # Nếu muốn xài ở các method khác thì phải có self
        try:
            profile_list = self.pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR) # Là phương thức của đối tượng Pipeline để lấy danh sách các cấu hình luồng (stream profile) cho cảm biến màu (color sensor)
            try:
                color_profile: VideoStreamProfile = profile_list.get_video_stream_profile(848, 0, OBFormat.RGB, 60)
            except OBError as e:
                print("Không lấy profile từ camera được : ", e)
                color_profile = profile_list.get_video_stream_profile()
                print("Color Profile: ", color_profile)
            self.config.enable_stream(color_profile)
        except Exception as e:
            print("Lỗi khi cấu hình camera : ", e)
            return
        self.pipeline.start(self.config) # Khởi động kết nối luồng camera với config có sẵn
        print("Camera Started")

        self.btn_trigger.setText("Trigger") # Chạy khi khởi tạo đối tượng app
        self.btn_trigger.clicked.connect(self.trigger_camera)
    def trigger_camera(self): # Đại diện cho chính đối tượng đó thuộc về
        try:
            frame: FrameSet = self.pipeline.wait_for_frames(1000)
            if frame is None:
                print("Không nhận được frame")
                return
            color_frame = frame.get_color_frame() # Lấy khung hình màu từ khung hình frame set vừa nhận được
            if color_frame is None:
                print("Không nhận được khung hình màu")
                return
            color_image = frame_to_bgr_image(color_frame)
            if color_image is None:
                print("Không nhận được ảnh màu")
                return
            # Chuyển đổi BGR sang RGB cho QT Creator
            frame_rgb = cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            q_image = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            # Ta có frame_rgb.data là trả về dữ liệu thô để phù hợp với QT
            pixmap = QPixmap.fromImage(q_image)
            self.lbl_display.setPixmap(pixmap.scaled(self.lbl_display.width(), self.lbl_display.height()))
        except Exception as e:
            print("Lỗi trigger : ", e)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec())
