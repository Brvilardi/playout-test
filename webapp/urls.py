from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("home", views.home, name="home"),
    path("video-upload", views.video_upload, name="video_upload"),
    path("your-videos", views.your_videos, name="your_videos")
]