import cv2

"""
Hãy tưởng tượng bạn có một nhóm bạn đang đứng ở các vị trí khác nhau trong một sân chơi
Bạn muốn tìm vị trí trung tâm của cả nhóm
Trong ví dụ này :
Mỗi người bạn tương ứng với một pixel của đối tượng
Vị trí (x, y) của mỗi người là tọa độ của pixel đó
Cân nặng của mỗi người tương ứng với cường độ sáng I(x, y) của pixel. (Giả sử người nặng hơn thì sáng hơn)
Ảnh trắng đen là 0 và 1
Bây giờ, hãy áp dụng các công thức :
1. m00 (Tổng cân nặng của cả nhóm)
Công thức : m00 = Σ (Cân nặng của mỗi người)
Tương ứng trong ảnh : m00 = Σ Σ I(x, y)
Ý nghĩa : Bạn cộng cân nặng của tất cả mọi người lại. Kết quả m00 là tổng cân nặng của cả nhóm
Nếu mọi người đều có cân nặng như nhau (bằng 1), thì m00 chính là tổng số người trong nhóm
2. m10 (Tổng momen theo chiều ngang)
Công thức : m10 = Σ (Vị trí x của mỗi người * Cân nặng của người đó)
Tương ứng trong ảnh : m10 = Σ Σ x * I(x, y)
Ý nghĩa : Bạn lấy vị trí theo chiều ngang (x) của từng người, nhân với cân nặng của họ, rồi cộng tất cả lại
Những người đứng xa hơn về bên phải (có x lớn) hoặc nặng hơn sẽ làm cho giá trị m10 này tăng lên nhiều
3. m01 (Tổng momen theo chiều dọc)
Công thức : m01 = Σ (Vị trí y của mỗi người * Cân nặng của người đó)
Tương ứng trong ảnh : m01 = Σ Σ y * I(x, y)
Ý nghĩa : Tương tự như trên, nhưng lần này bạn làm với vị trí theo chiều dọc (y)
Công thức cuối cùng : Tìm vị trí trung tâm (Cx, Cy)
Cx = m10 / m00
Tương tự : Tọa độ x trung tâm = (Tổng momen theo chiều ngang) / (Tổng cân nặng)
Ý nghĩa : Đây là tọa độ x trung bình của cả nhóm, có tính đến cân nặng của mỗi người
Cy = m01 / m00
Tương tự : Tọa độ y trung tâm = (Tổng momen theo chiều dọc) / (Tổng cân nặng)
Ý nghĩa : Đây là tọa độ y trung bình của cả nhóm
"""

img = cv2.imread('Images/Image 1.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
retval, img_binary = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY_INV)
cv2.imshow('Binary Image', img_binary)
contours, hierachy = cv2.findContours(img_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(f"Số lượng contours : {len(contours)}")
cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
for contour in contours:
    M  = cv2.moments(contour)
    Cx = int(M['m10']/M['m00'])
    Cy = int(M['m01']/M['m00'])
    print(f"Center of mass : ({Cx}, {Cy})")
    cv2.circle(img, (Cx, Cy), 2, (255, 0, 0), 2)
    cv2.putText(img, f"({Cx}, {Cy})", (Cx, Cy-20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
    cv2.imshow('Original Image', img)
# Giá trị -1 thì nó sẽ tô đặc hình tròn với màu đã chọn
# Trả về là một từ điển dictionary chứa các giá trị như m00, m10, m01
if cv2.waitKey(0) & 0xff == ord('q'):
    cv2.destroyAllWindows()
