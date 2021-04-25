from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.

class ScoreBoard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ScoreBoard_user')
    title = models.CharField(max_length=50, blank=True)


class Note(models.Model):
    drawingJSONText = models.TextField(null = True)