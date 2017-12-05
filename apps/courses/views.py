# coding:utf8
from django.shortcuts import render

from django.views.generic.base import View
from .models import Course

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class CourseListView(View):
    """
    课程列表
    """
    def get(self, request):
        all_course = Course.objects.all()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_course, 3, request=request)
        # 不是一个queryset对象，所以在模板中需要修改 {%for course in all_course.object_list%}
        courses = p.page(page)

        return render(request, 'course-list.html', {"all_course": courses})


