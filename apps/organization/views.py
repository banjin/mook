# coding:utf8
from django.shortcuts import render

from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.views.generic import View
from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite

class OrgView(View):
    """
    课程机构列表功能
    """
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()

        hot_orgs=all_orgs.order_by('-click_num')

        # 城市
        all_citys = CityDict.objects.all()

        # 对地区进行筛选
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get('ct', '')
        if city_id:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('course_nums')
        org_nums = all_orgs.count()
        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        return render(request, 'org-list.html', {'all_orgs': orgs,
                                                 'all_citys': all_citys,
                                                 'org_nums': org_nums,
                                                 'city_id': city_id,
                                                 'category': category,
                                                 'hot_orgs': hot_orgs,
                                                 'sort': sort})


class AddUserAskView(View):
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            # 异步操作,返回Json格式，而不是页面
            return HttpResponse("{'status': 'success'}", content_type='application/json')
        else:
            return HttpResponse("{'status': 'fail', 'msg': '添加出错'}", content_type='application/json')


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav =False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3]
        all_teacher = course_org.teacher_set.all()[:1]

        return render(request, 'org-detail-homepage.html', {'all_courses': all_courses,
                                                            "all_teacher": all_teacher,
                                                            "course_org": course_org,
                                                            'current_page': current_page,
                                                            'has_fav':has_fav})


class OrgCourseView(View):
    """
    机构课程
    """

    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_courses = course_org.course_set.all()[:3]
        return render(request, 'org-detail-course.html', {'all_courses': all_courses,
                                                          "course_org": course_org,
                                                          'current_page': current_page,
                                                          'has_fav': has_fav})


class OrgDescView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        return render(request, 'org-detail-desc.html', {'has_fav':has_fav,
                                                          "course_org": course_org,
                                                          'current_page': current_page})


class OrgTeacherView(View):
    """
    机构介绍
    """

    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teacher = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {"all_teacher": all_teacher,
                                                          "course_org": course_org,
                                                          'current_page': current_page,
                                                            'has_fav': has_fav})


class AddFavView(View):
    """
    用户收藏
    """
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否登录
        if not request.user.is_authenticated():
            return HttpResponse("{'status': 'fail', 'msg': '用户未登录'}", content_type='application/json')
        exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id),fav_type=fav_type)
        if exist_record:
            # 如果记录已经存在，表示取消收藏
            exist_record.delete()
            return HttpResponse("{'status': 'success', 'msg': '收藏'}", content_type='application/json')
        else:
            user_fav = UserFavorite()
            if fav_id>0 and fav_type >0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse("{'status': 'success', 'msg': '已经收藏'}", content_type='application/json')
            else:
                return HttpResponse("{'status': 'fail', 'msg': '收藏出错'}", content_type='application/json')


class TeacherListView(View):
    """
    讲师列表
    """
    def get(self, request):
        all_teachers = Teacher.objects.all()
        top_teachers = all_teachers.order_by('-click_num')
        teacher_num = all_teachers.count()
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_num')

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_teachers, 5, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {'all_teachers': teachers,
                                                      'teacher_num': teacher_num,
                                                      'top_teachers': top_teachers,
                                                      'sort': sort,})


class TeacherDetailView(View):
    """
    教师详情
    """
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=int(teacher_id))
        teacher.click_num +=1
        teacher.save()
        courses = teacher.course_set.all()
        has_teacher_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher_id):
            has_teacher_faved = True

        has_org_faved = False
        if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
            has_org_faved = True

        teachers = Teacher.objects.all().order_by("-click_num")[:3]
        return render(request, 'teacher-detail.html', {'teacher': teacher,
                                                       'courses':courses,
                                                       'teachers':teachers,
                                                       'has_teacher_faved':has_teacher_faved,
                                                       'has_org_faved':has_org_faved})
