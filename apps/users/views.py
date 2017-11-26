# coding:utf8
from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
# Create your views here.

from .models import UserProfile


class CustomBackend(ModelBackend):
    """通过邮箱登录的功能"""
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


def my_login(request):
    if request.method == "POST":
        user_name = request.POST.get('username', "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, 'index.html', {'msg':u'用户名和密码错误'})
    elif request.method == "GET":
        return render(request, 'login.html', {})


def my_logout(request):
    logout(request)
    return render(request, "index.html", {})