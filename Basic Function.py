import cv2

"""
# Đọc ảnh
img_color = cv2.imread('Friends.jpeg', 1) # 1 là ảnh màu, 0 là ảnh xám, -1 là ảnh màu với alpha channel
img_gray = cv2.imread('Friends.jpeg', 0) # 1 là ảnh màu, 0 là ảnh xám, -1 là ảnh màu với alpha channel
img_alpha = cv2.imread('Friends.jpeg', -1) # 1 là ảnh màu, 0 là ảnh xám, -1 là ảnh màu với alpha channel
# Kênh alpha chanel này đại diện cho độ trong suốt của ảnh
# Ảnh jpeg không hỗ trợ alpha channel
# Hiển thị ảnh
cv2.imshow('Friends', img_color)
cv2.imshow('Friends_Gray', img_gray)
cv2.imshow('Friends_Alpha', img_alpha)
# Chờ người dùng nhấn phím bất kỳ để thoát
cv2.waitKey(0) # 0 là chờ đến khi người dùng nhấn phím
cv2.destroyAllWindows() # Đóng tất cả các cửa sổ
"""

"""
img = cv2.imread('Friends.jpeg', 1)
print(img)
print(type(img)) # numpy.narray là kiểu dữ liệu đa chiều của thư viện NumPy
if img is not None:
    print("Ảnh đã được đọc thành công")
else:
    print("Không tìm thấy ảnh")
"""

"""
img = cv2.imread('Friends.jpeg', 1)
cv2.imshow('Friends', img)
retral = cv2.waitKey(0) # Mã ASCII của phím được nhấn
print(retral)
cv2.imwrite('Friends_Copy.jpeg', img) # Nếu mà lưu trong folder project thì chỉ ghi tên file thôi, còn chỗ khác thì ghi đường dẫn đầy đủ
if retral == 27: # 27 là mã ASCII của phím ESC
    cv2.destroyAllWindows()
"""

"""
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Không thể mở camera")
else:
    print("Camera đã được mở thành công")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Không thể đọc frame")
            break
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
"""

"""
img = cv2.imread('Friends.jpeg', 1)
cv2.line(img, (0,0), (400, 400), (0, 0, 255), 1, cv2.LINE_8) # shift = chia tọa độ cho 2^shift
cv2.rectangle(img, (100, 100), (300, 300), (0, 255, 0), 2, cv2.LINE_8)
cv2.circle(img, (200, 200), 50, (255, 0, 0), 2, cv2.LINE_8)
cv2.putText(img, 'Hello World', (100, 250), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_8, bottomLeftOrigin=False)
# Trục y trong OpenCV hướng xuống ngược với toán học
# Ta có bottomLeftOrigin nếu là true thì tọa độ của chữ sẽ hướng ngược xuống, mặc định là false chữ sẽ hướng lên
# Ta dùng shift khi muốn vẽ tọa độ thập phân, vì tọa độ phải là số nguyên, khi có sẵn tọa độ từ các thuật toán khác dưới dạng biến
# Hoặc là muốn vẽ chính xác đến nhỏ hơn 1 pixel
cv2.imshow('Friends', img)
print("Kích Thước Của Ảnh :",img.shape) # (height, width, channels) channel là số kênh màu BGR
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

"""
img = cv2.imread('Friends.jpeg', 1)
print("Kích Thước", img.shape)
img_resize = cv2.resize(img, (400, 400), interpolation=cv2.INTER_LINEAR)
cv2.imshow('Friends', img_resize)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

"""
img = cv2.imread('Friends.jpeg', 1)
print("Kích Thước", img.shape)
img_crop = img[100:300, 400:600]
cv2.rectangle(img, (400, 100), (600, 300), (0, 255, 0), 2, cv2.LINE_8)
cv2.imshow('Friends_1', img_crop)
cv2.imshow('Friends_2', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

"""
img = cv2.imread('Friends.jpeg', 1)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Ảnh Gốc', img)
cv2.imshow('Ảnh Xám', img_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Ảnh mức xám thường được dùng để nhận dạng chữ viết và trích xuất các đặc trưng
# Ảnh trắng đen thì dùng để phân tách đối tượng, tìm đường bao, nhận diện mã vạch và QR code
# Ngoài ra còn xử lý hình thái học (Morphological Operations)
# Dùng để làm giãn (Dilation) hoặc xói mòn (Erosion) đối tượng
# Giúp loại bỏ nhiễu hạt li ti hoặc lấp đầy các lỗ hổng trong vật thể
"""

"""
img = cv2.imread('Friends.jpeg', 1)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
retval, img_binary = cv2.threshold(img_gray,0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Dùng phân ngưỡng tự động để bằng cách thêm cờ cv2.THRESH_OTSU
# Ta có retval trả về giá trị ngưỡng được sử dụng trong quá trình phân đoạn ảnh
# Nếu dùng phân ngưỡng Otsu thì giá trị trả về là ngưỡng tìm được
print('Retral Value', retval)
cv2.imshow('Friends_1', img_binary)
cv2.imshow('Friends_2', img_gray)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

"""
img = cv2.imread('Friends.jpeg', 1)
img_blur = cv2.GaussianBlur(img, (15, 15), 0)
cv2.imshow('Friends_Blur', img_blur)
cv2.imshow('Friends', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""

"""
# Ảnh mờ dùng để làm mờ các chi tiết không quan trọng trong xử lý ảnh
1. ksize (Kích thước nhân lọc) - Là Kích Thước của Cây Cọ
    ksize = (3, 3) : Bạn dùng một cây cọ rất nhỏ. Khi bạn di cọ, nó chỉ làm nhòe một vùng rất bé. 
    Ảnh chỉ mờ đi một chút xíu.
    ksize = (25, 25) : Bạn dùng một cây cọ rất to. Khi bạn di cọ, nó làm nhòe một vùng màu cực lớn. 
    Ảnh sẽ bị mờ đi rất nhiều.
    => ksize quyết định vùng ảnh hưởng của thao tác làm mờ.
2. sigmaX - Là Lượng Nước trên Cây Cọ
    Bây giờ, hãy giả sử bạn luôn dùng một cây cọ có kích thước cố định (ví dụ ksize = (35, 35)). 
    Ta có sigmaX sẽ quyết định độ ướt của cây cọ đó.
    sigmaX nhỏ (ví dụ : 1.0) : Cọ ít nước.
    Khi bạn chấm cọ vào một điểm, chỉ có màu ở ngay tâm cọ bị hòa tan mạnh. 
    Màu ở rìa của cây cọ gần như không bị ảnh hưởng.
    Kết quả trên ảnh : Chỉ các pixel rất gần pixel trung tâm mới bị ảnh hưởng nhiều. 
    Ảnh chỉ mờ đi một cách nhẹ nhàng, tinh tế.
    sigmaX lớn (ví dụ : 10.0) : Cọ rất nhiều nước.
    Khi bạn chấm cọ vào một điểm, nước lan ra khắp đầu cọ. 
    Màu ở cả vùng trung tâm lẫn vùng rìa của cây cọ đều bị hòa tan và trộn lẫn vào nhau một cách mạnh mẽ.
    Kết quả trên ảnh : Các pixel ở xa pixel trung tâm cũng bị ảnh hưởng mạnh. 
    Ảnh bị mờ đi rất nhiều, trông như "nhòe" hẳn đi.
    => sigma quyết định cường độ hay mức độ làm mờ trong vùng ảnh hưởng đó.
3. sigma Y - Là Tương Tự
    Thường OpenCV sẽ để sigmaY = sigmaX
    => sigmaY quyết định cường độ hay mức độ làm mờ trong vùng ảnh hưởng đó.
ksize : Vùng làm mờ to hay nhỏ? (Cây cọ to hay nhỏ?)
sigma : Mức độ làm mờ mạnh hay yếu? (Cọ nhiều nước hay ít nước?)
sigma = 0 : Chế độ tự động, để OpenCV tự quyết định mức độ mờ dựa trên kích thước vùng mờ.
"""

"""
Ảnh canny hay thuật toán canny là một thuật toán được sử dụng trong xử lý hình ảnh để phát hiện các cạnh trong ảnh. 
Canny được phát triển bởi John F. Canny vào năm 1986 và được coi là một trong những thuật toán canny tốt nhất cho việc phát hiện cạnh.
Ứng dụng để tìm ra biên của đối tượng trong ảnh, nhận dạng và theo dõi đối tượng.
Nó sẽ qua các phương pháp như sau : làm mờ Gaussian -> tính toán độ dốc -> loại bỏ các điểm không cực đại -> áp dụng ngưỡng -> liên kết các cạnh để tạo ra đường biên hoàn chỉnh
"""

"""
img = cv2.imread('Friends.jpeg', 1)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
img_canny = cv2.Canny(img_blur, 100, 200)
cv2.imshow('Friends', img)
cv2.imshow('Friends_Canny', img_canny)
cv2.waitKey(0)
cv2.destroyAllWindows()
# Tham số thứ 2 là ngưỡng thấp, nếu thấp hơn là bị xóa
# Tham số thứ 3 là ngưỡng cao, nếu cao hơn là được giữ lại và được xem là cạnh biên
"""






