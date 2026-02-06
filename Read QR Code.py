import cv2
import pyzbar.pyzbar as pyzbar # Thư viên dùng để đọc barcode
import numpy as np

img = cv2.imread('Images/QR Code.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
decode_object = pyzbar.decode(img_gray)
for decode in decode_object:
    # Nó có kiểu dữ liệu là list bên trong chứa object
    text = decode.data.decode("utf-8")
    # Xài cái UTF để giải mà kiểu byte ra string theo định dạng utf-8
    qr_type = decode.type
    rect = decode.rect
    points = decode.polygon
    print(f"QR Code : {text}")
    print(f"QR Type : {qr_type}")
    print(f"QR Rectangle : {rect}")
    print(f"QR Polygon : {points}")
# x, y, w, h = decode_object[0].rect # Ta có chấm rect là để truy cập thuộc tính đối tượng
# polygon = decode_object[0].polygon
# x0, y0 = polygon[0]
# x1, y1 = polygon[1]
# x2, y2 = polygon[2]
# x3, y3 = polygon[3]
# cv2.circle(img, (x0, y0), 5, (0, 0, 255), cv2.FILLED)
# cv2.putText(img, "1", (x0 - 15, y0 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
# cv2.circle(img, (x1, y1), 5, (0, 0, 255), cv2.FILLED)
# cv2.putText(img, "1", (x1 - 15, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
# cv2.circle(img, (x2, y2), 5, (0, 0, 255), cv2.FILLED)
# cv2.putText(img, "1", (x2 + 5, y2 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
# cv2.circle(img, (x3, y3), 5, (0, 0, 255), cv2.FILLED)
# cv2.putText(img, "1", (x3 + 5, y3 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
# cv2.circle(img, (x + w // 2, y + h // 2), 5, (0, 0, 255), cv2.FILLED)
# cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
# cv2.putText(img, decode_object[0].data.decode("utf-8"), (x - 90, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
# polygon = np.array(decode_object[0].polygon, np.int32) # Đưa về dạng mạng để đưa vào hàm array, có thể sẽ lỗi vì numpy nó chỉ nhận tuple hay list thôi
# Nó không nhận kiểu dữ liệu object vì vậy có thể gây ra lỗi
polygon = np.array([(p.x, p.y) for p in decode_object[0].polygon]) # Dùng cách này gọi là list comprehension tạo ra tuple và đưa vào array
print(decode_object[0].polygon)
print(polygon)
cv2.drawContours(img, [polygon], 0, (0, 255, 0), 2)
# rect = cv2.minAreaRect(polygon) # Tìm hình chữ nhật nhỏ nhất bao quanh đa giác
# box = cv2.boxPoints(rect) # Chuyển rect thành 4 đỉnh của hình chữ nhật
cv2.imshow('QR Code', img_gray)
cv2.imshow('QR Code', img)
print("Code : ",decode_object)
cv2.waitKey(0)
cv2.destroyAllWindows()