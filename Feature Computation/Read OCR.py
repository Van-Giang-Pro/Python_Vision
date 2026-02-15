import pytesseract as ptr
import cv2
import re # Module này dùng để thay thế một phần chuổi bằng một phần khác

ptr.pytesseract.tesseract_cmd = r'C:\Users\fs120806\AppData\Local\Programs\Tesseract OCR\tesseract.exe'
img = cv2.imread('../Images/Text.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
retval, img_binary = cv2.threshold(img_gray, 160, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
cv2.imshow('Image', img_binary)
config = "--oem 3 --psm 6"
text = ptr.image_to_string(img_binary, lang='eng', config=config)
text = re.sub(r'[^a-zA-Z0-9- ]', '', text)
# Phải gán lại chuỗi mới vì re.sub trả về chuỗi mới
# Ta có Khi bạn đặt chữ r trước một chuỗi, bạn đang nói với Python rằng :
# Hãy coi tất cả các ký tự trong chuỗi này là ký tự thô, bình thường.
# Đừng diễn giải bất kỳ ký tự đặc biệt nào cả. Một dấu \ chỉ đơn giản là một dấu \.
# Ta có ^ là phủ định là NOT, còn text là chuỗi ký tự đầu vào.
# Sau cùng '' là chuỗi ký tự thay thế.
cv2.putText(img, text, (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1, cv2.LINE_AA)
# img_resized = cv2.resize(img, (1200, 400), interpolation=cv2.INTER_LINEAR) # Window to nhở thì chữ và ảnh cũng to nhỏ theo
# Thay đổi luôn bản chất tấm ảnh
cv2.namedWindow('OCR', cv2.WINDOW_NORMAL) # Để cho phép window có thể resize
cv2.resizeWindow('OCR', 1200, 600) # Để đặt kích thước window
cv2.imshow('Binary', img_binary) # Ảnh đưa vào bị thay đổi kích thước tạm thời, kéo giãn theo
cv2.imshow('OCR', img)
print(text)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
--oem 3 là gì ?
OEM = OCR Engine Mode 
Chế độ engine OCR
--oem 0: engine legacy cũ
--oem 1: LSTM engine mới, thường tốt hơn
--oem 2: kết hợp legacy + LSTM
--oem 3: tự động chọn (hay dùng nhất, an toàn)
Vậy --oem 3 nghĩa là : Tự chọn engine tốt nhất có sẵn

--psm 6 là gì ?
PSM = Page Segmentation Mode : chế độ phân tích bố cục trang 
Tesseract sẽ chia ảnh thành dòng hay khối chữ như thế nào
Một vài giá trị hay dùng :
--psm 6: 1 khối văn bản đồng nhất (nhiều dòng) → hợp với đoạn text như chat bubble
--psm 7: 1 dòng duy nhất (nếu ảnh chỉ có 1 dòng)
--psm 11: sparse text (chữ rải rác, không theo khối rõ ràng)
Vậy --psm 6 nghĩa là : Coi ảnh như một block chữ nhiều dòng
"""
