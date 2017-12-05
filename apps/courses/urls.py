# coding:utf-8

from django.conf.urls import include, url
from .views import CourseListView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
]
