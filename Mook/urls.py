# coding:utf8
"""Mook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.contrib import admin
from users.views import (my_login, my_logout, LoginView, RegisterView,
                         ActiveUserView, ForgetPwdView,ResetView, ModifyPwdView)
from organization.views import OrgView

import xadmin

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url('^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # url('^login/$', TemplateView.as_view(template_name='login.html'), name='login'),
    # 基于函数
    # url(r'login/$', my_login, name='login'),
    #  基于类
    url(r'login/$', LoginView.as_view(), name='login'),
    url(r'register/$', RegisterView.as_view(), name='register'),
    url(r'logout/$', my_logout, name='logout'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='active'),
    url(r'forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'modify_pwd/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构首页
    url(r'^org_list/$', OrgView.as_view(), name='org_list'),
]
