from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import time
from .funcs import *

# Create your models here.

class ScoreBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ScoreBoard_user')
    title = models.CharField(max_length=50, blank=True)


class Note(models.Model):
    drawingJSONText = models.TextField(null = True)

class NoteIMG(models.Model):
    file = models.ImageField(upload_to='images')
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
