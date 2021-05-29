from django.shortcuts import render, redirect
from .models import NoteIMG
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import ImageForm

from io import BytesIO
from PIL import Image
import re
import base64

import psycopg2

import random

import datetime

import base64
from django.core.files.base import ContentFile

from django.views.decorators.csrf import csrf_exempt

from .Model.model import getModel
from skimage.transform import resize
import numpy as np
from io import BytesIO
from .funcs import data_preprocessing

def index(request):
    return render(request,"score/score_index.html")

@csrf_exempt
def paint(request):
    if request.method == 'GET':
        return render(request, 'score/score_create.html')
    if request.method == 'POST':
        image = request.POST.__getitem__('image')

        format, imgstr = image.split(';base64,') 
        ext = format.split('/')[-1] 
        data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        '''conn = psycopg2.connect(database="djangopaint", user="nidhin")
        cur = conn.cursor()
        cur.execute("INSERT INTO files(name, image) VALUES(%s, %s)", [filename, data])
        conn.commit()
        conn.close()
        '''
        img_bytes = base64.b64decode(imgstr)
        img = Image.open(BytesIO(img_bytes))
        img  = np.array(img)
        img = data_preprocessing(img)

        target_names = ['quarter', 'half', '8th', '16th', 'dot_quarter', 'dot_half', 'dot_8th', 'dot_16th']

        model = getModel()
        cex = model.predict(img)
        output = np.argmax(cex)
        
        
        print(cex)
        print(target_names[output])

        '''
        return_val = model(IMG)
        return Http('/create', return_val)
        0 :
        1 :
        '''

        return HttpResponseRedirect('/create/')
