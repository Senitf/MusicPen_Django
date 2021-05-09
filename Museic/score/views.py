from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from .models import *
import json
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import re
from .forms import ImageForm

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
    model = NoteIMG
    fields = ['title', 'image']
    template_name_suffix = 'create'
    success_url = '/'

def upload(request):
    form = ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return JsonResponse({'message':'works'})
    context = {'form':form}
    return render(request, 'score/score_create.html', context)
    '''
    if request.method == 'POST':
        new_content = NoteIMG()
        new_content.title = str(time.time())
        tmpIMG = request.FILES.get('canvasData')
        print(tmpIMG)
        new_content.image = tmpIMG
        
        pattern = r'^data:(?P<mime_type>[^;]+);base64,(?P<image>.+)$'
        result = re.match(pattern, tmpIMG)
        if result:
            mime_type = result.group('mime_type')
            new_content.image = result.group('image').decode('base64')
        
        new_content.save()
        return redirect('score:create')
    else:
        return render(request, 'score/score_create.html')
    '''