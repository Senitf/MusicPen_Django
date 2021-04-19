from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import *
import json
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

class Index(TemplateView):
    template_name = 'score/score_index.html'
    '''
    def ajax_method(self, request):
        #POST 방식은 GET 방식과 달리, 데이터 전송을 기반으로 한 요청
        if request.method == "POST":

            #javascrpit에서 데이터를 가져와 DataFrame으로 변형(데이터분석을 위해)
            uploaded = request.POST.get('upload_data', None)
            uploaded_list = json.loads(uploaded)

        #COUNTRY, CURRENCY, SECTOR를 concat하여 모아 json형태로 변형한다. 
            port_total_json = uploaded.to_json(orient='records')

            context = {
                'port_total_json' : port_total_json,
            }
        #javascript에 json형태로 데이터를 보낸다.
            return HttpResponse(port_total_json)
    '''

class Create(CreateView):
    model = Note
    fields = ['drawingJSONText']
    template_name = 'score/score_create.html'
    success_url = '/'