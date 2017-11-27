# coding:utf-8

from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=6)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
