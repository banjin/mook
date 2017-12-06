# coding:utf-8

from django.conf.urls import include, url
from .views import CourseListView, CourseDetailView

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^course_detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
]
