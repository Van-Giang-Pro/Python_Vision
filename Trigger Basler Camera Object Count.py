import cv2
from pypylon import pylon
import numpy as np

define_frame_width = 800
try:
    # Tạo một đối tượng camnera và truy cập vào camera đầu tiên nhìn thấy
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
    camera.LineSelector.Value = "Line1"
    camera.LineMode.Value = "Input"
    camera.ExposureAuto.Value = "Off"
    camera.ExposureTime.Value = 290000.0
    # camera.ExposureAuto.Value = "Continuous"
    while camera.IsGrabbing():
        count = 0
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
        input_status = camera.LineStatus.Value
        if input_status:
            print("Input Signal Detected")
        else:
            print("No Input Signal Detected")
        if grab_result.GrabSucceeded() and input_status:
            img_data = converter.Convert(grab_result).GetArray()
            height, width, channels = img_data.shape
            new_frame_width = define_frame_width
            new_frame_height = int(height * new_frame_width / width)
            resized_image = cv2.resize(img_data, (new_frame_width, new_frame_height), interpolation=cv2.INTER_LINEAR)
            img_gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
            retval, img_binary = cv2.threshold(img_blur,60 , 255, cv2.THRESH_BINARY)
            contours, hierachy = cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                if 1000 < cv2.contourArea(contour) < 25000:
                    count = count + 1
                    min_rect = cv2.minAreaRect(contour)
                    rect_box = cv2.boxPoints(min_rect)
                    rect_box_int = np.int32(rect_box)
                    cv2.drawContours(resized_image, [rect_box_int], -1, (0, 255, 0), 2)
            cv2.putText(resized_image, f"Count : {count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
            cv2.imshow("Camera Viewer", img_binary)
            cv2.imshow("Original Image", resized_image)
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