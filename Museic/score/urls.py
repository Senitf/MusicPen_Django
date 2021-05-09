from django.urls import path
from .views import *

app_name = "score"
urlpatterns = [
    path("create/", upload, name="create"),
]

