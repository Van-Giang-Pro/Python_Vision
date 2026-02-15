import cv2
import numpy as np

"""
Độ bão hòa (Saturation) giống như việc bạn thêm màu trắng hoặc màu xám vào lon sơn đó.
Độ bão hòa cao (100%) : Màu sơn đỏ của bạn rất đậm, rực rỡ và tinh khiết.
Độ bão hòa thấp (gần 0%) : Khi bạn pha thêm nhiều màu trắng hoặc xám, màu đỏ sẽ nhạt dần,
trở nên bạc màu và cuối cùng biến thành màu xám. Nó mất đi cường độ màu.
Giá trị (Value) giống như việc bạn đặt lon sơn đó trong một căn phòng có thể điều chỉnh độ sáng hoặc tối.
Giá trị cao (100%) : Căn phòng sáng hết mức. Bạn thấy rõ màu đỏ rực rỡ của sơn.
Giá trị thấp (gần 0%) : Khi bạn giảm độ sáng của đèn, căn phòng tối dần.
Màu đỏ của bạn cũng tối đi và cuối cùng trở thành màu đen. Nó mất đi độ sáng.
"""

img = cv2.imread('../Images/Shapes With Color.png', 1)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
lower_red = np.array([20, 100, 100]) # Ta có np.array giống như cái khay đựng trứng chỉ chứa các con số thôi
upper_red = np.array([30, 255, 255])
img_mask = cv2.inRange(img_hsv, lower_red, upper_red)
cv2.imshow('Original', img)
cv2.imshow('Result', img_mask)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
Nếu pixel đó nằm trong khoảng từ lower_red đến upper_red : Nó sẽ biến pixel đó thành màu Trắng (giá trị 255).
Nếu pixel đó nằm ngoài khoảng : Nó sẽ biến pixel đó thành màu Đen (giá trị 0).
Kết quả trả về (mask) là một bức ảnh chỉ có hai màu đen và trắng (gọi là ảnh nhị phân hoặc mặt nạ - mask).
"""