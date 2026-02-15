import cv2
from pypylon import pylon
import numpy as np
import pyzbar.pyzbar as pyzbar # Thư viện để đọc mã QR và Barcode
from sympy.core.sympify import converter

define_frame_width = 800
try:
    # Tạo một đối tượng camera và truy cập vào camera đầu tiên nhìn thấy
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    print("Đã tìm thấy camera : ", camera.GetDeviceInfo().GetModelName())
    camera.Open()
    camera.OffsetX.Value = 0
    camera.OffsetY.Value = 0
    camera.Width.Value = 2276
    camera.Height.Value = 2358
    camera.OffsetX.Value = 568
    camera.OffsetY.Value = 0
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed
    # Trong tài liệu của Basler có nói port opto thì không cấu hình được
    camera.LineSelector.Value = "Line3"
    camera.LineMode.Value = "Input"
    camera.LineSelector.Value = "Line4"
    camera.LineMode.Value = "Output"
    camera.LineSource.Value = "UserOutput3"
    camera.ExposureAuto.Value = "Off"
    camera.ExposureTime.Value = 100000
    # camera.ExposureAuto.Value = "Off"
    while camera.IsGrabbing():
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        input_status = camera.LineStatus.Value
        if input_status:
            print("Input Signal Detected")
        else:
            print("No Input Signal Detected")
        if grab_result.GrabSucceeded():
            text = ""
            img_data = converter.Convert(grab_result).GetArray()
            height, width, channels = img_data.shape
            new_frame_width = define_frame_width
            new_frame_height = int(height * new_frame_width / width)
            resized_image = cv2.resize(img_data, (new_frame_width, new_frame_height), interpolation=cv2.INTER_LINEAR)
            img_gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
            decode_object = pyzbar.decode(img_blur)
            print(decode_object)
            if decode_object:
                for object in decode_object:
                    text = object.data.decode("utf-8") # Xài cái UTF để giải mã kiểu byte ra string theo định dạng utf-8
                    polygon = np.array([(p.x, p.y) for p in decode_object[0].polygon]) # Dùng cách này gọi là list comprehension tạo ra tuple và đưa vào array
                    cv2.drawContours(resized_image, [polygon], 0, (0, 255, 0), 2)
                    cv2.putText(resized_image, text, (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                camera.LineSelector.Value = "Line4"
                camera.UserOutputValue.Value = True
                status = camera.LineStatus.Value
                print("Trạng thái ngõ ra pin 3 line 4 : ", status)
                time.sleep(1)
                camera.LineSelector.Value = "Line4"
                camera.UserOutputValue.Value = False
                status = camera.LineStatus.Value
                print("Trạng thái ngõ ra pin 3 line 4 : ", status)
            cv2.imshow("Resized Image", resized_image)
            cv2.imshow("QR Code", resized_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            grab_result.Release()
except pylon.GenericException as e:
    print("Đã xảy ra lỗi : ", e)
except Exception as e:
    print("Đã xảy ra lỗi không xác định : ", e)
finally:
    if 'camera' in locals():
        camera.Close()
        cv2.destroyAllWindows()

"""
Ta có locals() là một hàm trong Python trả về một từ điển (dictionary) 
Nó chứa tất cả các biến cục bộ đang tồn tại tại thời điểm đó.
Ta có 'camera' in locals() kiểm tra xem cái tên biến có tên là camera đã được định nghĩa và đang tồn tại hay chưa.
Nếu camera không kết nối được, dòng camera = pylon.InstantCamera(...) sẽ gây ra lỗi và nhảy sang khối except. 
Lúc này biến camera chưa tồn tại.
Khi chương trình chạy xuống khối finally, nếu bạn gọi ngay camera.Close() mà không kiểm tra, Python sẽ báo lỗi : NameError : name 'camera' is not defined.
Vì vậy, việc kiểm tra 'camera' in locals() giúp đảm bảo chương trình chỉ gọi lệnh Close() khi biến camera đã được khởi tạo thành công trước đó.
"""


