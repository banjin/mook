# coding:utf8
from django.shortcuts import render

from django.views.generic.base import View
from .models import Course,CourseResource, Video
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserFavorite, CourseComment, UserCourse
from utils.mixin_utils import LoginRequiredMixin
from django.db.models import Q


class CourseListView(View):
    """
    课程列表
    """
    def get(self, request):
        all_course = Course.objects.all().order_by('-add_time')
        fav_courses = Course.objects.all().order_by('-fav_nums')[:3]

        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords)|Q(desc__icontains=search_keywords)|Q(degree__icontains=search_keywords))

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


class CourseInfoView(LoginRequiredMixin, View):
    """
    章节信息
    """
    def get(self, request, course_id):
        course = Course.objects.get(pk=int(course_id))

        # 查询用户是否已经关联该课程
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        lessons = course.lesson_set.all()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = all_user_course.values_list('id', flat=True)
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        course_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-video.html', {"course": course,
                                                     "lessons": lessons,
                                                     "course_resources":course_resources,
                                                     'relate_courses':relate_courses})


class CommentView(LoginRequiredMixin, View):
    """
    课程评论
    """
    def get(self, request, course_id):
        course = Course.objects.get(pk=int(course_id))
        lessons = course.lesson_set.all()
        course_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComment.objects.filter(user=request.user, course=course)
        return render(request, 'course-comment.html', {"course": course,
                                                     "lessons": lessons,
                                                     "course_resources":course_resources,
                                                     'all_comments':all_comments})


class AddCommentView(View):
    """
    添加评论
    """

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse("{'status': 'fail', 'msg': '用户未登录'}", content_type='application/json')
        course_id = request.POST.get('course_id', 0)
        comments = request.POST.get("comments", '')
        if course_id > 0 and comments:
            course_comments = CourseComment()
            course = Course.objects.get(pk=int(course_id))
            course_comments.course = course
            course_comments.comment = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse("{'status': 'success', 'msg': '添加成功'}", content_type='application/json')

        else:
            return HttpResponse("{'status': 'fail', 'msg': '添加失败'}", content_type='application/json')


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(pk=int(video_id))
        course = video.lesson.course
        # 查询用户是否已经关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        lessons = course.lesson_set.all()
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_course = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = all_user_course.values_list('id', flat=True)
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')
        course_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {"course": course,
                                                     "lessons": lessons,
                                                     "course_resources": course_resources,
                                                     'relate_courses': relate_courses,
                                                     'video':video})