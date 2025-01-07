from django.contrib.auth.hashers import check_password
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import *

# Create your views here.
def home(request):
    data = Info.objects.all()
    print(data)
    return render(request, 'home.html', {'data': data})

@csrf_protect
def register(request):
    if request.method == 'POST':
        Name = request.POST['name']
        Email = request.POST['email']
        Password = request.POST['password']
        Re_password = request.POST['re-password']
        if Info.objects.get(Email=Email) == Email:
            e = "Email already exists"
            return render(request, 'Register.html', {'e':e})
        else:
            if Password == Re_password:
                data = Info(Name=Name,Email=Email,Password=Password)
                data.save()
                return redirect(home)
            else:
                err = "Password does not match!!"
                return render(request, 'Register.html', context={'err': err})
    return render(request, 'Register.html')

@csrf_protect
def login(request):
    if request.method == 'POST':
        Email = request.POST['email']
        Password = request.POST['pass']
        try:
            user = Info.objects.get(Email=Email)  # Use Info model's 'Email' field
        except Info.DoesNotExist:
            err = "Email does not exist!"
            return render(request, 'Login.html', context={'err': err})

            # Check if the password matches using the check_password method (for hashed passwords)
        if check_password(Password, user.Password):
            return redirect('home')  # Redirect to home page after successful login
        else:
            err = "Password is incorrect!"
            return render(request, 'Login.html', context={'err': err})

    return render(request, 'Login.html')