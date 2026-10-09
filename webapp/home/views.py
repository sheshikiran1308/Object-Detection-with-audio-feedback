from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import base64
from django.views.decorators.csrf import csrf_exempt


def detect_and_draw_box(filename, model="yolov3.weights", confidence=0.6):
    img_filepath = "home/static/home/images/"+filename
    img = cv2.imread(img_filepath)
    bbox, label, conf = cv.detect_common_objects(img, model=model)
    print(f"========================nImage processed: {filename}n")
    output_image = draw_bbox(img, bbox, label, conf)
    cv2.imwrite('home/static/home/images/'+filename, output_image)
    d = {'label': label, 'conf': conf}
    print(d)
    return d

def index(request):
    return render(request,'index.html')

@csrf_exempt
def savepic(request):
    img_uri = request.body
    img_uri = str(img_uri)
    data = img_uri[25:]
    data =base64.b64decode(data)
    f = open('home/static/home/images/img.jpg','wb')
    f.write(data)
    f.close()
    d = detect_and_draw_box("img.jpg")
    return JsonResponse(d)