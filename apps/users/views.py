# coding:utf8
from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# Create your views here.
from django.views.generic.base import View

from .models import UserProfile
from .forms import LoginForm, RegisterForm
from utils.email_send import send_register_email


class CustomBackend(ModelBackend):
    """通过邮箱登录的功能"""
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user:
                login(request, user)
                return render(request, "index.html")
            else:
                return render(request, 'login.html', {'msg': u'用户名和密码错误'})
        else:
            return render(request, 'login.html', {"login_form": login_form})


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', "")
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


def my_login(request):
    if request.method == "POST":
        user_name = request.POST.get('username', "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, 'login.html', {'msg': u'用户名和密码错误'})
    elif request.method == "GET":
        return render(request, 'login.html', {})


def my_logout(request):
    logout(request)
    return render(request, "index.html", {})
