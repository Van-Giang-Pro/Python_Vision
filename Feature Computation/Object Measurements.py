import cv2
import numpy as np

img = cv2.imread("../Images/Iphone 15.jpg")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (5, 5), sigmaX=0)
actual_object_length = 147.6
# img_blur = cv2.medianBlur(img_gray, 5)
retval, img_binary = cv2.threshold(img_blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# cv2.imshow("Blur", img_blur)
contours, hierachy = cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    area = cv2.contourArea(contour)
    if area > 10000:
        min_rect = cv2.minAreaRect(contour)
        box = cv2.boxPoints(min_rect)
        # Trả về kiểu numpy array
        # Hàm này sẽ tạo ra 4 điểm của hình chữ nhật dựa vào kết quả của min_rect
        box = np.int32(box)
        min_rect_width = min_rect[1][0]
        min_rect_height = min_rect[1][1]
        # min_rect_width, min_rect_height = min_rect[1]
        object_length = max(min_rect_width, min_rect_height)
        mm_per_pixel = actual_object_length / object_length
        # cv2.putText(img, "1", box[0], cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        # cv2.putText(img, "2", box[1], cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        # cv2.putText(img, "3", box[2], cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        # cv2.putText(img, "4", box[3], cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
        cv2.drawContours(img, [box], 0, (0, 255, 0), 2)
        caculated_object_width = mm_per_pixel * min_rect_width
        caculated_object_height = mm_per_pixel * min_rect_height
        cv2.putText(img, f"Width : {caculated_object_width:.2f} mm", (box[0][0] - 157, box[0][1] + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.putText(img, f"Height : {caculated_object_height:.2f} mm", (box[0][0] - 157, box[0][1] + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
print(f"Số lượng contours : {len(contours)}")
cv2.imshow("Binary", img_binary)
cv2.imshow("Battery", img_gray)
cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
Vì cv2.drawContours yêu cầu tham số contours phải là một list các contour, chứ không nhận một contour đơn lẻ theo dạng mảng điểm trực tiếp. 
Ta có box của bạn là một mảng NumPy dạng (4, 2) và (4 điểm x,y) tạo ra 1 contour. 
Ta có drawContours lại muốn contours có dạng : [contour1, contour2]. 
Nên bạn phải bọc nó thành list : [box] (tức là danh sách chỉ có 1 contour).
"""