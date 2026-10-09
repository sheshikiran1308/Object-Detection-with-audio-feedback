import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
def detect_and_draw_box(filename, model="yolov3.weights", confidence=0.6):
    img_filepath = "images/"+filename
    img = cv2.imread(img_filepath)
    cv2.imshow('img',img)
    cv2.waitKey(0)
    bbox, label, conf = cv.detect_common_objects(img, model=model)
    print(f"========================nImage processed: {filename}n")
    for l, c in zip(label, conf):
        print(f"Detected object: {l} with confidence level of {c}n")
    output_image = draw_bbox(img, bbox, label, conf)
    cv2.imwrite('images_with_boxes/'+filename, output_image)
    d = {'label': label, 'conf': conf}
    return d

detect_and_draw_box('text.jpg')