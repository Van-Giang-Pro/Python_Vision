import cv2
import numpy as np
import math

arrow_length = 50
img = cv2.imread("../Images/12 Tab Defect.bmp")
# x, y, w, h = 200, 260, 60, 60
# roi = img[y:y+h, x:x+w]
# Ta có y đứng trước là ảnh là mảng NumPy, img là kiểu dữ liệu NumPy
# Ta có x được mặc định là hàng, y được mặc định là cột
# cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
retval, img_binary = cv2.threshold(img_blur, 80, 255, cv2.THRESH_BINARY)
contours, hierachy = cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(f"Số lượng contours : {len(contours)}")
# cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
for contour in contours:
    if cv2.contourArea(contour) < 3000:
        continue
    # Nếu nhỏ hơn ngưỡng này thì nó sẽ bỏ qua contour hiện tại
    # Và quay lại đầu vòng for để xử lý contour tiếp theo
    M = cv2.moments(contour)
    Cx = int(M['m10']/M['m00'])
    Cy = int(M['m01']/M['m00'])
    print(f"Center of mass : ({Cx}, {Cy})")
    cv2.circle(img, (Cx, Cy), 2, (255, 0, 0), 2)
    min_rect = cv2.minAreaRect(contour) # Trả về kiểu tuple ([x, y], [width, height], angle)
    angle = int(min_rect[2])
    print(f"Góc angle : {angle}")
    print(f"Chiều rộng : {min_rect[1][0]}")
    print(f"Chiều cao : {min_rect[1][1]}")
    if min_rect[1][0] > min_rect[1][1]:
    # Chúng ra sẽ chuẩn hóa nếu w > h hay w < h thì đều tính theo trục Y của object so với trục X
        angle = angle + 90
    print(f"Tâm hình chữ nhật : ({min_rect[0][0]}, {min_rect[0][1]})")
    print(f"Kích thước hình chữ nhật : ({min_rect[1][0]}, {min_rect[1][1]})")
    print(f"Góc xoay : {angle}")
    rect_box = cv2.boxPoints(min_rect) # Trả về kiểu numpy array
    # Hàm này sẽ chuyển đổi thông tin đó thành danh sách 4 điểm cụ thể để bạn có thể vẽ
    rect_box_int = np.int32(rect_box)
    cv2.drawContours(img, [rect_box_int], 0, (0, 255, 0), 2)
    cv2.putText(img, f"Angle : {angle} Deg", (Cx, Cy - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(img, f"X : {Cx}, Y : {Cy}", (Cx, Cy-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)
    Cx_angle_arrow_line_right_x = int(Cx + (arrow_length * math.cos(math.radians(angle))))
    Cy_angle_arrow_line_right_y = int(Cy + (arrow_length * math.sin(math.radians(angle))))
    Cx_angle_arrow_line_left_x = int(Cx - (arrow_length * math.cos(math.radians(90 - angle))))
    Cy_angle_arrow_line_left_y = int(Cy + (arrow_length * math.sin(math.radians(90 - angle))))
    print(Cx_angle_arrow_line_right_x)
    print(Cy_angle_arrow_line_right_y)
    print(Cx_angle_arrow_line_left_x)
    print(Cy_angle_arrow_line_left_y)
    cv2.arrowedLine(img, (Cx, Cy), (Cx_angle_arrow_line_right_x, Cy_angle_arrow_line_right_y), (0, 255, 0), 2)
    cv2.arrowedLine(img, (Cx, Cy), (Cx_angle_arrow_line_left_x, Cy_angle_arrow_line_left_y), (0, 255, 0), 2)
    # roi_resized = cv2.resize(roi, (300, 200), interpolation=cv2.INTER_LINEAR)
    # Tìm tâm của ROI
    BA = 107 # Này là chúng ta tự xác định sao đó từ cái này tính ra góc beta rồi tính BA, BC theo góc beta
    BC = 22 # Vì khi nó xoay là tọa độ của tâm ROI so với hệ tọa độ là đã thay đổi rồi nên cần tính theo góc
    # Cx_roi = Cx - BA # Tâm ROI so với tâm của vật thể, tọa độ góc dùng để dò tâm ROI
    # Cy_roi = Cy + BC # Tâm ROI so với tâm của vật thể, tọa độ góc dùng để dò tâm ROI
    beta = math.degrees(math.atan((BC / BA)))
    AC_length = math.sqrt((BC * BC) + (BA * BA))
    alpha = 90 - beta
    BA_length = AC_length * math.cos(math.radians(180 - alpha - angle))
    BC_length = AC_length * math.sin(math.radians(180 - alpha - angle))
    Xcenter_ROI = Cx - BA_length
    Ycenter_ROI = Cy + BC_length
    # Các hàm lượng giác đều luôn nhận góc vào theo đơn vị radian
    # cv2.circle(img, (Cx_roi, Cy_roi), 5, (0, 0, 255), -1) # Dùng để dò tâm ROI
    cv2.circle(img, (int(Xcenter_ROI), int(Ycenter_ROI)), 5, (0, 0, 255), -1)
    # Tính và vẽ hình chữ nhật vùng ROI (xoay theo góc)
    width_ROI = 50
    height_ROI = 50
    roi_rect = ((Xcenter_ROI, Ycenter_ROI), (width_ROI, height_ROI), angle)
    roi_box = cv2.boxPoints(roi_rect) # Hàm này dùng để lấy ra 4 đỉnh của hình chữ nhật
    roi_box_int = np.int32(roi_box) # Chuyển đổi thành kiểu dữ liệu integer
    cv2.drawContours(img, [roi_box_int], 0, (0, 255, 0), 2)
    # Bọc roi_box_int vì hàm vẽ contour yêu cầu mảng điểm ở dươi dạng list
    # Hiển thị vùng ROI thành 1 vùng tách riêng biệt
    roi_crop = img[int(Ycenter_ROI) - (height_ROI // 2):int(Ycenter_ROI) + (height_ROI // 2), int(Xcenter_ROI) - (width_ROI // 2):int(Xcenter_ROI) + (width_ROI // 2)]
    roi_crop_resized = cv2.resize(roi_crop, (300, 200), interpolation=cv2.INTER_LINEAR)
    # Chuyển đổi ảnh vùng ROI thành ảnh nhị phân
    roi_gray = cv2.cvtColor(roi_crop_resized, cv2.COLOR_BGR2GRAY)
    roi_blur = cv2.GaussianBlur(roi_gray, (5, 5), 0)
    retval, roi_binary = cv2.threshold(roi_blur, 80, 255, cv2.THRESH_BINARY_INV)
    # Kiểm tra contour trong hình ảnh
    contours, hirachy = cv2.findContours(roi_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        cv2.putText(img, "OK", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    else:
        cv2.putText(img, "NO", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    # Hiển thị hình ảnh
    cv2.imshow('Binary Image', img_binary)
    cv2.imshow('Original Image', img)
    cv2.imshow("ROI Image", roi_binary)
if cv2.waitKey(0) & 0xff == ord('q'):
    cv2.destroyAllWindows()
print("Done")

"""
Ta có interpolation là phương pháp nội suy ảnh để giảm kích thước ảnh hay phóng to ảnh
cv2.INTER_AREA : Thường được khuyên dùng khi thu nhỏ ảnh để tránh hiện tượng răng cưa.
cv2.INTER_CUBIC hoặc cv2.INTER_LINEAR : Tốt cho việc phóng to ảnh. 
INTER_CUBIC cho chất lượng cao hơn nhưng chậm hơn một chút. 
INTER_LINEAR là lựa chọn mặc định, cân bằng giữa tốc độ và chất lượng.
cv2.INTER_NEAREST : Nhanh nhất nhưng cho chất lượng thấp nhất, thường tạo ra ảnh bị khối vuông
"""

