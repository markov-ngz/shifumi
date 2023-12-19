from django.contrib.auth import views as auth_views
from django.urls import path
from . import views 
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path("",views.home, name="home"),
    path('signup/',views.signup, name='signup'),
    path('logout/',auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('login/', auth_views.LoginView.as_view(next_page='/',template_name='core/login.html', authentication_form=LoginForm), name='login')
]