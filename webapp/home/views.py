from django.http.response import JsonResponse
from django.shortcuts import render
import cv2
import cvlib as cv
from cvlib.object_detection import draw_bbox
import base64
import numpy as np
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt


def detect_and_draw_box(filename, model="yolov3.weights", confidence=0.6):
    img_filepath = "home/static/home/images/" + filename
    img = cv2.imread(img_filepath)
    if img is None:
        return {'label': [], 'conf': [], 'message': 'Unable to read captured image'}

    bbox, label, conf = cv.detect_common_objects(img, model=model)
    print(f"========================\nImage processed: {filename}\n")
    output_image = draw_bbox(img, bbox, label, conf)
    cv2.imwrite('home/static/home/images/' + filename, output_image)
    d = {'label': label, 'conf': conf, 'message': 'Object detected' if label else 'No object detected'}
    print(d)
    return d


def index(request):
    return render(request, 'index.html')


def decode_image_data_uri(raw_body):
    if raw_body is None:
        raise ValueError('No image data received')

    body = raw_body.decode('utf-8', errors='ignore') if isinstance(raw_body, bytes) else str(raw_body)
    body = unquote(body).strip()

    if body.startswith('data:'):
        body = body.split(',', 1)[1]
    elif body.startswith('data='):
        body = body.replace('data=', '', 1)

    return base64.b64decode(body)


@csrf_exempt
def savepic(request):
    try:
        image_bytes = decode_image_data_uri(request.body)
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        if image is None:
            return JsonResponse({'label': [], 'conf': [], 'message': 'Unable to decode the camera image'}, status=400)

        image_path = 'home/static/home/images/img.jpg'
        cv2.imwrite(image_path, image)
        d = detect_and_draw_box('img.jpg')
        return JsonResponse(d)
    except Exception as exc:
        return JsonResponse({'label': [], 'conf': [], 'message': str(exc)}, status=400)