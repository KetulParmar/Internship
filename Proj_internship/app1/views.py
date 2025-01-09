from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
import random
from .forms import Cap
from .models import *


# Create your views here.
def home(request):
    data = Info.objects.all()
    return render(request, 'home.html', {'data': data})


@csrf_protect
def register(request):
    if request.method == 'POST':
        Name = request.POST['name']
        Email = request.POST['email']
        Password = request.POST['password']
        Re_password = request.POST['re-password']
        if Password == Re_password:
            data = Info(Name=Name, Email=Email, Password=Password)
            data.save()
            return redirect(home)
        else:
            err = "Password does not match!!"
            return render(request, 'Register.html', context={'err': err})
    return render(request, 'Register.html')


@csrf_protect
def login(request):
    form1 = Cap(request.POST)
    if request.method == 'POST':
        Email = request.POST['email1']
        Password = request.POST['pass1']
        try:
            rC = Info.objects.get(Email=Email)
            if rC.Password == Password:
                return redirect(home)
            else:
                err = "Incorrect Password!"
                return render(request, 'Login.html', context={'err': err})
        except:
            err = "Something went wrong"
            return render(request, 'Login.html', context={'err': err})
    return render(request, 'Login.html')


def forget(request, id):
    if request.method == 'POST':
        Otp1 = random.randint(1000, 9999)

        send_mail('Forget Password',
                  #settings.EMAIL_HOST_USER,

                  )

    return render(request, 'forget.html')


def Otp(request, id):
    pass


def edit(request, id):
    data = Info.objects.get(id=id)
    if request.method == 'POST':
        Name = request.POST['name']
        Email = request.POST['email']
        Password = request.POST['password']

        data.Name = Name
        data.Email = Email
        data.Password = Password
        data.save()
        return redirect(home)
    else:
        return render(request,'Edit.html')

def delete(request, id):
    data = Info.objects.get(id=id)
    data.delete()
    return redirect(home)