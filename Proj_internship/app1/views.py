from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect

from .models import *
# Create your views here.
def home(request):
    return render(request, 'home.html')

@csrf_protect
def register(request):
    if request.method == 'POST':
        Name = request.POST['name']
        Email = request.POST['email']
        Password = request.POST['password']
        Re_password = request.POST['re-password']
        if Password == Re_password:
            data = Info(Name=Name,Email=Email,Password=Password)
            data.save()
            Msg = "Success"
            return render(request, 'home.html', context={'MSSG': Msg})
        else:
            err = "Password does not match!!"
            return render(request, 'Register.html', context={'err': err})
    return render(request, 'Register.html')

@csrf_protect
def login(request):
    if request.method == 'POST':
        Email = request.POST['email']
        Password = request.POST['pass']
        if Email == Info.objects.get('email'):
            if Password == Info.objects.get('Password'):
                return redirect(home)
            else:
                err = "Password Incorrect!!"
                return render(request, 'Login.html', context={'Err': err})
        else:
            err = "Email Does not exists!!"
            return render(request, 'Login.html', context={'Err': err})

    return render(request, 'Login.html')