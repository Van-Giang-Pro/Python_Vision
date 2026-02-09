import cv2
from pypylon import pylon
import time

defined_frame_width = 800
try:
    # Tạo một đối tượng camera để truy cập vào đôối tượng camera đầu tiên nhìn thấy
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    print("Đã tìm thấy camera : ", camera.GetDeviceInfo().GetModelName())
    camera.Open()
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
    converter = pylon.ImageFormatConverter() # Tạo đối tượng chuyển đổi định dạng ảnh
    converter.OutputPixelFormat = pylon.PixelType_BGR8packed # Chuyển đổi ảnh đầu ra thành BGR8 để cho opencv có thể xử lý
    camera.LineSelector.Value = "Line1"
    camera.LineMode.Value = "Input"
    camera.ExposureTime.Value = 10000.0
    while camera.IsGrabbing():
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        input_status = camera.LineStatus.Value
        # input_status = True
        if input_status:
            print("Input Signal Detected")
        else:
            print("No Input Signal Detected")
        if grab_result.GrabSucceeded():
            img_data = converter.Convert(grab_result).GetArray()
            height, width, channels = img_data.shape
            new_frame_width = defined_frame_width
            new_frame_height = int(height * new_frame_width / width)
            resized_image = cv2.resize(img_data, (new_frame_width, new_frame_height), interpolation=cv2.INTER_LINEAR)
            cv2.imshow("Original Image", resized_image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except pylon.GenericException as e:
    print("Đã xảy ra lỗi : ", e)
except Exception as e:
    print("Đã xảy ra lỗi không xác định : ", e)
finally:
    cv2.destroyAllWindows()