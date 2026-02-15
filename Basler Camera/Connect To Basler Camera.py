import cv2
from pypylon import pylon
import numpy as np
import pyzbar.pyzbar as pyzbar # Thư viên dùng để đọc barcode
from skimage.draw import polygon

defined_frame_width = 1100
try:
    # Tạo 1 đối tượng camera để truy cập vào camera đầu tiên tìm thấy
    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
    print("Đã tìm thấy camera : ", camera.GetDeviceInfo().GetModelName())
    # Mở camera
    camera.Open()
    # Cấu hình một số thông số cơ bản
    # camera.ExposureAuto.Value = "Continuous"
    # camera.AutoTargetBrightness.Value = 0.6
    # camera.BalanceWhiteAuto.Value = "Continuous"
    # camera.Gain.Value = 5
    # Bắt lấy hình ảnh
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) # Chỉ lấy ảnh mới nhất, bỏ qua các ảnh trong buffer
    # Tạo vòng lặp để liên tục lấy ảnh và hiển thị
    while camera.IsGrabbing(): # Ta có camera.IsGrabbing() trả về True khi camera vẫn đang lấy ảnh
        grab_result = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException) # Đợi 5000ms th tạo ra timeout
        # Kiểm tra xem ảnh có được lấy thành công không
        if grab_result.GrabSucceeded():
            image_data = grab_result.Array # Lấy mảng dữ liệu numpy array
            # Xử lý ảnh với Open CV
            pixel_format = grab_result.PixelType
            if (pixel_format == pylon.PixelType_BayerBG8):
                img_bgr = cv2.cvtColor(image_data, cv2.COLOR_BAYER_BG2BGR)
            elif (pixel_format == pylon.PixelType_BayerGB8):
                img_bgr = cv2.cvtColor(image_data, cv2.COLOR_BAYER_GB2BGR)
            elif (pixel_format == pylon.PixelType_BayerRG8):
                img_bgr = cv2.cvtColor(image_data, cv2.COLOR_BAYER_RG2BGR)
            elif (pixel_format == pylon.PixelType_BayerGR8):
                img_bgr = cv2.cvtColor(image_data, cv2.COLOR_BAYER_GR2BGR)
            elif (pixel_format == pylon.PixelType_Mono8):
                img_bgr = cv2.cvtColor(image_data, cv2.COLOR_GRAY2BGR)
            else:
                img_bgr = image_data
            # Thay đổi kích thước hiển thị hình ảnh
            height, width, channels = img_bgr.shape # Ta có shape là thuộc tính của numpy
            new_width = defined_frame_width
            new_height = int(new_width * height / width)
            # print(new_width, new_height)
            resized_image = cv2.resize(img_bgr, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
            # Window to nhỏ thì chữ và ảnh cũng to nhỏ theo
            # Thay đổi luôn bản chất tấm ảnh
            img_gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            decode_object = pyzbar.decode(img_gray, symbols=[pyzbar.ZBarSymbol.QRCODE])
            # Chỉ định loại code cần đọc giúp tăng tốc và hạn chế lỗi
            for decode in decode_object:
                text = decode.data.decode("utf-8")
                # print(text)
                print(decode)
                cv2.putText(resized_image, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,1, (0, 255, 0), 2)
                polygon = np.array([(p.x, p.y) for p in decode.polygon])
                # Ta có p chỉ là đại diện cho object xong p.x và p.y là thuộc tính của p
                cv2.drawContours(resized_image, [polygon], 0, (0, 255, 0), 2)
                # Lấy một đỉnh của hình vuông
                p0 = decode.polygon[0]
                x, y = p0.x, p0.y
                cv2.putText(resized_image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                # Ta có pylon là do hàm draw contour chỉ nhận list contours
            # cv2.imshow('Basler Camera', img_gray)
            cv2.imshow('Resized Image', resized_image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        grab_result.Release()
    camera.StopGrabbing()
    camera.Close()
except pylon.GenericException as e:
    print("Đã xảy ra lỗi : ", e)
except Exception as e:
    print("Đã xảy ra lỗi khác: ", e)
finally:
    cv2.destroyAllWindows()

"""
Khi thay đổi kích thước ảnh, OpenCV phải tính toán giá trị pixel mới. Ta có INTER_LINEAR là nội suy song tuyến tính. 
Lấy trung bình có trọng số từ 4 pixel xung quanh.
Các phương pháp phổ biến : INTER_NEAREST, INTER_LINEAR, INTER_CUBIC, INTER_AREA
"""
