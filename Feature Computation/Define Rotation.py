import cv2
import numpy as np
import math

arrow_length = 50
img = cv2.imread('../Images/12 Tab Defect.bmp')
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
    print(f"Tâm hình chữ nhật : ({min_rect[0][0]}, {min_rect[0][1]})")
    print(f"Kích thước hình chữ nhật : ({min_rect[1][0]}, {min_rect[1][1]})")
    print(f"Góc xoay : {angle}")
    rect_box = cv2.boxPoints(min_rect) # Trả về kiểu numpy array
# Hàm này sẽ chuyển đổi thông tin đó thành danh sách 4 điểm cụ thể để bạn có thể vẽ
    rect_box_int = np.int32(rect_box)
    # cv2.drawContours(img, [rect_box_int], 0, (0, 0, 255), 2)
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
    cv2.imshow('Binary Image', img_binary)
    cv2.imshow('Original Image', img)
if cv2.waitKey(0) & 0xff == ord('q'):
    cv2.destroyAllWindows()


