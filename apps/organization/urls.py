# coding:utf-8

from django.conf.urls import include, url
from .views import (OrgView, AddUserAskView, OrgHomeView,OrgCourseView,
                    OrgDescView,OrgTeacherView, AddFavView, TeacherDetailView, TeacherListView)

urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)$', OrgTeacherView.as_view(), name='org_teacher'),

    # 教师列表
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)$', TeacherDetailView.as_view(), name='teacher_detail'),

    # 机构收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),
]


