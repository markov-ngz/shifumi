from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import cv2
from django.views.decorators.csrf import csrf_exempt
import threading
import json
from PIL import Image
import base64
import io
import numpy as np
from .preprocess import * 
from .predict import *
from .rpc import jouer


def another(request):
    return render(request,"janken_video/camera2.html")

@csrf_exempt 
def frame_streaming(request):
    try:
        data_received = json.loads(request.body)
        print('Data received:', data_received.keys())
    except json.JSONDecodeError as e:
        print('Error decoding JSON:', e)

    image_b64  = data_received['image']

    base64_decoded = base64.b64decode(image_b64+ "==")


    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)

    np.save("image_test.npy",image_np)

    image_rgb = image_np[:,:,:3]

    print("Dimension de l'image enregistrée : ", image_rgb.shape)

    #----PREPROCESS + PREDICTION --------------------------------------------------------------------------------------------

    image_preprocessed = preprocess_image(image_rgb)

    label_predicted = predict_coup(image_preprocessed)

    #-------------------------------------------------------------------------------------------------

    resultat_partie = jouer(label_predicted)

    resultat = json.dumps(resultat_partie)

    # Create an HttpResponse object
    response = HttpResponse(content=resultat, content_type='application/json')

    # response['content'] = resultat

    # response['content_type'] = "application/json"

    # Add the Access-Control-Allow-Origin header
    response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000/liveplay/livestream'

    # You can also add other CORS headers if needed
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'

    return response

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        _, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@gzip.gzip_page
def livefe(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:  # This is bad! replace it with proper handling
        pass