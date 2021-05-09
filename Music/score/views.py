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

# Create your views here.
def upload(request):
    if request.method == 'POST':

        canvasData = request.POST.get('canvasData', '')
        
        datauri = canvasData

        imgstr = re.search(r'base64,(.*)', datauri).group(1)

        output = open('output.png', 'wb')

        output.write(imgstr.decode('base64'))

        output.close()

        new_content = NoteIMG()
        new_content.file = output
        new_content.save()
        return render(request, 'score/score_upload.html')
    else:
        return render(request, 'score/score_upload.html')

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
        new_content = NoteIMG()
        new_content.file = data
        new_content.save()

        return HttpResponseRedirect('/create/')