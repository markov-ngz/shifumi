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
import os

def another(request):
    print(os.getcwd())
    return render(request,"janken_video/camera2.html")


@csrf_exempt # !!! NEVER DO THIS EXCEPT IF YOU KNOW, WAS DONE JUST CAUSE I WAS LAZY  
def frame_streaming(request):

    # ugly way to deal with an image
    try:
        
        data_received = json.loads(request.body)
        print('Data received:', data_received.keys())
    except json.JSONDecodeError as e:
        print('Error decoding JSON:', e)

    # get the image value
    image_b64  = data_received['image']

    # add the == to decode the image
    base64_decoded = base64.b64decode(image_b64+ "==")

    # 
    image = Image.open(io.BytesIO(base64_decoded))
    image_np = np.array(image)

    image_rgb = image_np[:,:,:3]

    print("Dimension de l'image enregistrée : ", image_rgb.shape)

    #----PREPROCESS + PREDICTION --------------------------------------------------------------------------------------------

    image_preprocessed = preprocess_image(image_rgb)

    label_predicted = predict_coup(image_preprocessed)

    #-------------------------------------------------------------------------------------------------

    resultat_partie = jouer(label_predicted)

    resultat = json.dumps(resultat_partie)

    # Create an HttpResponse object and returning it 
    response = HttpResponse(content=resultat, content_type='application/json')
    response['Access-Control-Allow-Origin'] = 'http://127.0.0.1:8000/liveplay/livestream'
    response['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response['Access-Control-Allow-Headers'] = 'Content-Type'

    return response