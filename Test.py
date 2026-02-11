import cv2
import numpy as np

def fill_holes(binary):
    # Fill những chấm đen trên vật thể màu trắng nằm trên nền đen của ảnh nhị
    # Có tác dụng loại bỏ nhiễu trắng vùng lớn trên nền và chấm đen trên nền trắng của vật thể
    h, w = binary.shape
    flood = binary.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, mask, seedPoint=(0, 0), newVal=255)
    # Hàm này chỉ lan từ tọa độ (0, 0) và chỉ tô nền thành trắng
    flood_inv = cv2.bitwise_not(flood)
    return cv2.bitwise_or(binary, flood_inv)

img = cv2.imread("Images/Test 1.png")
if img is None:
    raise FileNotFoundError("Không đọc được ảnh")

# Làm việc trên kênh sáng để ít bị ảnh hưởng màu
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB) #
L, A, B = cv2.split(lab) # Tách thành 3 kênh riêng biệt mỗi kênh sẽ là 1 ảnh

# Tăng tương phản để vật thể nổi hơn nền
clahe = cv2.createCLAHE(clipLimit=1.0, tileGridSize=(8, 8))
L_space_img = clahe.apply(L)

# Giảm nhiễu nhẹ
L_space_img_blur = cv2.GaussianBlur(L_space_img, (5, 5), 0)
retval, img_binary = cv2.threshold(L_space_img_blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Tạo kernel cho phép mở và đóng
k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (4, 4))
k_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

# Thực hiện phép mở và đóng
close_img = cv2.morphologyEx(img_binary, cv2.MORPH_CLOSE, k_close, iterations=1)
# open_img = cv2.morphologyEx(close_img, cv2.MORPH_OPEN, k_open, iterations=1)

dialate_img = cv2.dilate(close_img, k_close, iterations=2)

filled_hole_img = fill_holes(dialate_img)

contours, hirerachy = cv2.findContours(filled_hole_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for contour in contours:
    min_rect = cv2.minAreaRect(contour)
    rect_box = cv2.boxPoints(min_rect)
    rect_box_int = np.int32(rect_box)
    cv2.drawContours(img, [rect_box_int], -1, (0, 255, 0), 2)

print(len(contours))

cv2.imshow("Original", img)
cv2.imshow("Result", filled_hole_img)

if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()

