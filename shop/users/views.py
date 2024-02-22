from django.shortcuts import render, HttpResponse, redirect

from .forms import Login, Registration

from django.contrib.auth import authenticate, login, logout


# Create your views here.

def home_view(request):
    return HttpResponse('hello users')

def registration_view(request):
    if request.method == 'POST':
        form = Registration(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = Registration()
    context = {
        'form': form
    }
    return render(request, 'users/registration.html', context)


def login_view(request):
    if request.method == 'POST':
        form =Login(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('store:home')
    else:
        form = Login()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)

def logout_view(request):
    logout(request)
    return redirect('store:home')


