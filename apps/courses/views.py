# coding:utf8
from django.shortcuts import render

from django.views.generic.base import View
from .models import Course,CourseResource

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite

class CourseListView(View):
    """
    课程列表
    """
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        fav_courses = Course.objects.all().order_by('-fav_nums')[:3]
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_course.order_by('-students')
            elif sort == 'hot':
                all_course = all_course.order_by('-fav_nums')
        course_nums = all_course.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_course, 3, request=request)
        # 不是一个queryset对象，所以在模板中需要修改 {%for course in all_course.object_list%}
        courses = p.page(page)

        return render(request, 'course-list.html', {"all_course": courses,
                                                    "course_nums":course_nums,
                                                    'sort': sort,
                                                    'fav_courses':fav_courses})


class CourseDetailView(View):
    """
    课程详情
    """
    def get(self, request, course_id):
        course = Course.objects.get(pk=int(course_id))
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1).exists():
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2).exists():
                has_fav_org = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag).exclude(id=course.id)[:1]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {'course': course,
                                                      "relate_courses": relate_courses,
                                                      'has_fav_course': has_fav_course,
                                                      'has_fav_org': has_fav_org})



class CourseInfoView(View):
    """
    章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(pk=int(course_id))
        lessons = course.lesson_set.all()
        course_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {"course": course,
                                                     "lessons": lessons,
                                                     "course_resources":course_resources})
