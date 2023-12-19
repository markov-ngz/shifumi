from django.urls import path
from . import views 

app_name = 'janken_video'

urlpatterns = [
    path("livestream",views.another,name="video_test"),
    path("frame-streaming", views.frame_streaming, name="frame-streaming")
]