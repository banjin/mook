# coding:utf-8


from django.conf.urls import url, include

from .views import (UserinfoView, UploadImageView,UpdatePwdView,
                    MyCourseView, MyFavorgView, MyFavcourseView,
                    MyFavteacherView,MyMessageView)

urlpatterns = [
    url(r'^info/$', UserinfoView.as_view(), name='user_info'),
    url(r'^image/upload$', UploadImageView.as_view(), name='image_upload'),
    url(r'^password/upload$', UpdatePwdView.as_view(), name='password_upload'),
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),
    url(r'^my_fav_org/$', MyFavorgView.as_view(), name='my_fav_org'),
    url(r'^my_fav_teacher/$', MyFavteacherView.as_view(), name='my_fav_teacher'),
    url(r'^my_fav_course/$', MyFavcourseView.as_view(), name='my_fav_course'),
    url(r'^my_message/$', MyMessageView.as_view(), name='my_message'),
]