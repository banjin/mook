# coding:utf8
from django.shortcuts import render

from django.views.generic.base import View
from .models import Course


class CourseListView(View):
    """
    课程列表
    """
    def get(self, request):
        all_course = Course.objects.all()
        return render(request, 'course-list.html', {"all_course":all_course})


