from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NoteIMG(models.Model):
    file = models.ImageField(upload_to='images/')
    uploaded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class Note(models.Model):
    index = models.CharField(max_length=50, blank=False) #어떤 종류의 음악 기호인지 음표, 쉼표
    value = models.IntegerField(default=0) #4분, 8분

    def __str__(self):
        return str(self.pk)

class Score(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=50, default='Untitled')
    content = models.ManyToManyField(Note, related_name='notes')

    def __str__(self):
        return self.title + "_" + self.artist

