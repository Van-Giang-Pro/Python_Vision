from fast_alpr import ALPR
import cv2

img_path = "../Images/License Plate 3.png"
alpr = ALPR(detector_model="yolo-v9-t-384-license-plate-end2end",
            ocr_model="cct-xs-v1-global-model",)
img = cv2.imread(img_path)
cv2.imshow("License Plate Detection", img)
annotated_image = alpr.draw_predictions(img)
cv2.imshow("Annotated Image", annotated_image)
alpr_result = alpr.predict(img_path)
# print(alpr_result)
print(f"Biển Số : {alpr_result[0].ocr.text}")
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
Chạy 2 lệnh này để cài bộ công cụ Openvino để tăng tóc AI trên phần cứng Intel
pip install openvino
pip install fast-alpr[onnx]
Tham khảo API : https://github.com/ankandrew/fast-alpr?tab=readme-ov-file
"""


