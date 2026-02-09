import cv2
import numpy as np

def fill_holes(binary):
    """Fill lỗ bên trong vật thể trắng (255) trên nền đen (0)"""
    h, w = binary.shape[:2]
    flood = binary.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, mask, seedPoint=(0, 0), newVal=255)  # tô nền
    flood_inv = cv2.bitwise_not(flood)                        # đảo -> phần lỗ
    return cv2.bitwise_or(binary, flood_inv)                  # lấp lỗ

img = cv2.imread("Images/Test 1.png")
if img is None:
    raise FileNotFoundError("Không đọc được ảnh")

# 1) Làm việc trên kênh sáng để ít bị ảnh hưởng màu
lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
L, A, B = cv2.split(lab)

# 2) Tăng tương phản để vật thể nổi hơn nền
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
L2 = clahe.apply(L)

# 3) Giảm nhiễu nhẹ
L2 = cv2.GaussianBlur(L2, (5, 5), 0)

# 4) Nhị phân hoá: vật thể sáng => dùng THRESH_BINARY + OTSU
_, mask = cv2.threshold(L2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# 5) Morphology để nối liền phần kim loại + thân màu, bỏ hạt nhiễu
k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
k_open  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k_close, iterations=2)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  k_open,  iterations=1)

# 6) Lấp lỗ trong vật thể (nếu có)
mask = fill_holes(mask)

# 7) Tìm contour
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Lọc theo diện tích để bỏ nhiễu nhỏ
min_area = 1500
good = [c for c in contours if cv2.contourArea(c) > min_area]

# 8) Vẽ kết quả
out = img.copy()
cv2.drawContours(out, good, -1, (0, 255, 0), 2)

print("So contour bat duoc:", len(good))

cv2.imshow("L channel (clahe)", L2)
cv2.imshow("Mask", mask)
cv2.imshow("Contours", out)
cv2.waitKey(0)
cv2.destroyAllWindows()