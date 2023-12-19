from django.urls import path
from . import views 

app_name = 'janken'

urlpatterns = [
    path("",views.Play.as_view(), name="play"),
    path("/choice",views.game_choice,name="choice"),
]