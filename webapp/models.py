from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Video(models.Model):
    title = models.CharField(max_length=64, default="Untitled")
    thumbnail = models.ImageField(default="default_thumb.jpg", upload_to="thumbnails")
    video = models.FileField(upload_to="videos", default="error.mp4")
    video_url = models.CharField(max_length=255, default="error")
    duration = models.CharField(max_length=16, default="00:00")
    ownear = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.title} by {self.ownear.username}'

