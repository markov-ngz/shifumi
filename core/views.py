
from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect

@require_http_methods(["GET"])
def home(request):
    return render(request,
                  "core/home.html")

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html',{
        'form':form 
    })
@csrf_protect
@login_required
def logout_view(request):
    logout(request)
    return redirect('/')