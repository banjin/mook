# coding:utf-8

from django.conf.urls import include, url
from .views import OrgView, AddUserAskView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
]


