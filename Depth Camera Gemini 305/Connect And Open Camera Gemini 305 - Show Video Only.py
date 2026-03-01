import cv2
from pyorbbecsdk import *
from pyorbbecsdk import OBSensorType, VideoStreamProfile, OBFormat, OBError, FrameSet
from utils import frame_to_bgr_image

def main():
    config = Config() # Là đối tượng thiết lập cấu hình cho camera Orbbec, lưu trữ các thiết lập cấu hình như độ phân giải, tốc độ khung hình, định dạng dữ liệu để truyền vào pipeline khi khởi động camera
    pipeline = Pipeline() # Tạo một đối tượng Pipeline từ SDK Orbbec, nó quản lý luồng dữ liệu từ camera, cấu hình, kết nối, nhận frame từ camera
    try:
        profile_list = pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR) # Là phương thức của đối tượng Pipeline để lấy danh sách các cấu hình luồng (stream profile) cho cảm biến màu (color sensor)
        # Là 1 object of class StreamProfileList
        count = profile_list.get_count()
        for i in range(count):
           # Ta có print(profile_list[i])
           if isinstance(profile_list[i], VideoStreamProfile):
               # Hàm profile_list nó trả về danh sách các cấu hình luồng (stream profile) cho cảm biến màu (color sensor), thuộc nhiều profile khác nhau
               width = profile_list[i].get_width()
               height = profile_list[i].get_height()
               fps = profile_list[i].get_fps()
               fmt = profile_list[i].get_format()
               # print(f"width: {width}, height: {height}, fps: {fps}, fmt: {fmt}")
        try:
            color_profile: VideoStreamProfile = profile_list.get_video_stream_profile(848, 0, OBFormat.RGB, 60) # Chọn profile
            # Ta có 0 cho height nghĩa là heigth đó sẽ theo width
            print("Color Profile: ", color_profile)
            # Cách viết type hinting variable_name: Type = value dùng để ghi chú kiểu dữ liệu thôi
        except OBError as e:
            print(e)
            color_profile = profile_list.get_video_stream_profile() # Nếu không tìm thấy profile phù hợp, sẽ lấy profile mặc định
            print("Color Profile: ", color_profile)
        config.enable_stream(color_profile) # Thêm cấu hình luồng màu vào đối tượng Config để chuẩn bị khởi động camera với cấu hình này
    except Exception as e:
        print(e)
        return
    pipeline.start(config)
    while True:
        try:
            frame: FrameSet = pipeline.wait_for_frames(1000) # Đợi nhận được một bộ khung hình (frame set) từ camera trong vòng 1000ms
            if frame is None:
                continue # Chạy tiếp bỏ qua vòng lặp xong quay lại check frame mới
            color_frame = frame.get_color_frame() # Lấy khung hình màu từ bộ khung hình (frame set) vừa nhận được
            if color_frame is None: # Frame có thể trả về depth frame, color frame, ir frame
                continue
            color_image = frame_to_bgr_image(color_frame)
            if color_image is None:
                print("Failed to convert frame to image")
                continue
            cv2.imshow("Color Viewer", color_image) # Hiển thị khung hình màu đã được chuyển đổi sang định dạng BGR bằng OpenCV
            key = cv2.waitKey(1)
            if key == ord('q'):
                break
        except KeyboardInterrupt:
            break
    cv2.destroyAllWindows()
    pipeline.stop() # Dừng luồng dữ liệu từ camera và giải phóng tài nguyên

if __name__== "__main__":
    main()

"""
Hàm get_stream_profile_list(OBSensorType.COLOR_SENSOR) trả về một StreamProfileList (danh sách các profile).

Danh sách này có thể chứa nhiều loại profile khác nhau, tùy theo sensor :
VideoStreamProfile (cho video stream: color, depth, IR – có width, height, fps, format).
AccelStreamProfile hoặc GyroStreamProfile (cho accelerometer/gyroscope nếu sensor hỗ trợ IMU).
Có thể có các loại khác (IMU, custom) tùy camera.

Nếu bạn gọi thuộc tính get_width() trên một profile không phải VideoStreamProfile → sẽ bị AttributeError (không có method đó).

Hàm isinstance(profile, VideoStreamProfile) giúp :
Tránh lỗi runtime.
Chỉ xử lý các profile video (phù hợp với color/depth/IR).
In ra thông tin an toàn (nếu không phải, in thông báo khác).

Cần thêm file utlis.py để chạy hàm frame_to_bgr_image nha, file đó trong folder SDK.
"""
