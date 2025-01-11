from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.core.mail import send_mail
import random
from .forms import Cap
from .models import *
from django.conf import settings


# Create your views here.
@login_required
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
        Hash = make_password(Password)
        if Password == Re_password:
            data = Info(Name=Name, Email=Email, Password=Hash)
            data.save()
            data2 = User(username=Email, password=Hash)
            data2.save()
            return redirect(home)
        else:
            err = "Password does not match!!"
            return render(request, 'Register.html', context={'err': err})
    return render(request, 'Register.html')


@csrf_protect
def Login(request):
    c1 = Cap(request.POST)
    if request.method == 'POST':
        Email = request.POST['email1']
        Password = request.POST['pass1']
        try:
            us = User.objects.get(username=Email)
            print('1')
            cc = authenticate(username=Email, password=Password)
            print('2')
            if us is not None:
                print('3')
                if c1.is_valid():
                    print('4')
                    login(request, cc)
                    print('5')
                    return redirect(home)
                else:
                    err = "Incorrect captcha!"
                    return render(request, 'Login.html', context={'err': err})
            else:
                err = "Incorrect Password!"
                return render(request, 'Login.html', context={'err': err})
        except:
            err = "Something went wrong"
            return render(request, 'Login.html', context={'err': err})
    return render(request, 'Login.html', {'c1': c1})


def forget(request, id):
    if request.method == 'POST' and 'Email' in request.POST:
        email = request.POST.get('Email', '')
        try:
            user = Info.objects.filter(Email=email).count()
            if user == 1:
                user = Info.objects.get(Email=email)
                id = user.id

                otp = random.randint(1000, 9999)
                request.session['random1'] = otp

                send_mail(
                    'Forget Password',
                    f'Your one time password is {otp}',
                    settings.EMAIL_HOST_USER,
                    [email, ]
                )
                print(otp)
                red = redirect(f'/otp/{id}')
                red.set_cookie('Otp12', True, max_age=1000)
                return red

            else:
                return render(request, 'forget.html', context={'id': id, 'Err': 'Email Not Registered!'})

        except Info.DoesNotExist:
            return render(request, 'forget.html', context={'id': id, 'Err': 'Email Not Registered!'})

        except Exception as e:
            return render(request, 'forget.html', context={'id': id, 'Err': f'An error occurred: {str(e)}'})
    else:
        return render(request, 'forget.html', context={'id': id})


def Otp(request, id):
    print('came here1')
    if request.method == 'POST':
        print('came here2')
        if 'otp' in request.POST and request.POST['otp'] != '':
            print('came here3')
            if request.COOKIES.get('Otp12'):
                print('came here4')
                if 'p3' in request.POST and 'p4' in request.POST:
                    print('came here4')
                    pw1 = request.POST['p3']
                    pw2 = request.POST['p4']
                    Otp_Sms = int(request.session.get('random1'))
                    if Otp_Sms == int(request.POST['otp']):
                        print('came here5')
                        if pw1 == pw2:
                            try:
                                print('came here6')
                                u_pass = Info.objects.get(id=id)
                                c_pass = u_pass.Password

                                if pw1 is not u_pass:
                                    print('came here7')
                                    u_pass.Password = pw1
                                    u_pass.save()

                                    try:
                                        Uss = Info.objects.get(Email=u_pass.Email)
                                        Uss.password = make_password(pw1)
                                        Uss.save()
                                        print("Came here")
                                        return redirect(login)

                                    except Info.DoesNotExist:
                                        return HttpResponse('Django Auth User not found.')

                                else:
                                    err = "You cannot use the old password."
                                    return render(request, 'otp.html', {'err': err, 'id': id})
                            except:
                                return HttpResponse('User ID does not exist.')
                        else:
                            err = "Password is not same"
                            return render(request, 'otp.html', {'err': err, 'id': id})
                    else:
                        err = "Incorrect otp"
                        return render(request, 'otp.html', {'err': err, 'id': id})
                else:
                    err = "You cannot use the old password."
                    return render(request, 'otp.html', {'err': err, 'id': id})
            else:
                err = "otp expired"
                return render(request, 'otp.html', {'err': err, 'id': id})
        else:
            err = "Something went wrong!!"
            return render(request, 'otp.html', {'err': err, 'id': id})
    else:
        return render(request, 'otp.html')


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
        return render(request, 'Edit.html', context={'data': data})


def delete(request, id):
    data = Info.objects.get(id=id)
    data.delete()
    """u = User.objects.get(Email=Email)
    u.delete()"""
    return redirect(home)


def show(request, id):
    pass
