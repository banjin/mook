# coding:utf8
from django.shortcuts import render
from django.contrib.auth import authenticate,login, logout
import json

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.db.models import Q
# Create your views here.
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from .models import UserProfile, EmailVerifyRecord, Banner
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse, UserFavorite,UserMessage
from organization.models import CourseOrg,Teacher
from courses.models import Course


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


class CustomBackend(ModelBackend):
    """通过邮箱登录的功能"""
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': u'用户未激活'})
            else:
                return render(request, 'login.html', {'msg': u'用户名和密码错误'})
        else:
            return render(request, 'login.html', {"login_form": login_form})


class LogoutView(View):
    def get(self,request):
        logout(request)
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))


class ActiveUserView(View):
    def get(self,request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for recode in all_records:
                email = recode.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class RegisterView(View):
    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', "")
            if UserProfile.objects.filter(email=user_name):
                return render(request, 'register.html', {'register_form': register_form, 'msg': u'用户已经存在'})
            pass_word = request.POST.get("password", "")
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            user_message = UserMessage.objects.create(user=user_profile.id, message='欢迎注册')

            send_register_email(user_name, 'register')
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'register_form': register_form})


def my_login(request):
    if request.method == "POST":
        user_name = request.POST.get('username', "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username=user_name, password=pass_word)
        if user:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, 'login.html', {'msg': u'用户名和密码错误'})
    elif request.method == "GET":
        return render(request, 'login.html', {})


def my_logout(request):
    logout(request)
    return render(request, "index.html", {})


class ForgetPwdView(View):
    def get(self,request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {'forget_form':forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_register_email(email, send_type='forget')
            return render(request, 'send_success.html')
        else:
            return render(request, "forgetpwd.html", {'forget_form': forget_form, 'msg': u"邮箱错误"})


class ResetView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for recode in all_records:
                email = recode.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_fail.html')
        return render(request, 'login.html')


class ModifyPwdView(View):
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html', {'email': email, 'msg': u'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, 'login.html')
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'email': email, 'modify_form': modify_form})


class UserinfoView(LoginRequiredMixin, View):

    """
    用户个人信息
    """
    def get(self, request):
        return render(request, 'usercenter-info.html', {})


class UploadImageView(LoginRequiredMixin, View):
    """
    用户修改头像
    """
    def post(self, request):
        # 上传文件 利用form表单上传文件
        # image_form = UploadImageForm(request.POST, request.FILES)
        # if image_form.is_valid():
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            # request.user.save()
        # 利用modelform的特性直接save
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            request.user.save()
            return HttpResponse('{"status":"success"}',content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')





class UpdatePwdView(View):
    """
    个人中心修改密码
    """
    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return render(request, '{"status":"fail", "msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            return render(request, '{"status":"success", "msg":"修改成功"}', content_type='application/json')
        else:

            return render(json.dumps(modify_form.errors), content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {"user_courses":user_courses})


class MyFavorgView(LoginRequiredMixin, View):
    """
    我收藏的机构
    """
    def get(self,request):
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2).values_list('fav_id')
        org_list = CourseOrg.objects.filter(pk__in=fav_orgs)
        return render(request, 'usercenter-fav-org.html', {"org_list":org_list})

class MyFavteacherView(LoginRequiredMixin, View):
    """
    我收藏的教师
    """
    def get(self,request):
        fav_teacher_ids = UserFavorite.objects.filter(user=request.user, fav_type=3).values_list('fav_id')
        teacher_list = Teacher.objects.filter(pk__in=fav_teacher_ids)
        return render(request, 'usercenter-fav-teacher.html', {"teacher_list":teacher_list})


class MyFavcourseView(LoginRequiredMixin, View):
    """
    我收藏的课程
    """
    def get(self,request):
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1).values_list('fav_id')
        course_list = Course.objects.filter(pk__in=fav_courses)
        return render(request, 'usercenter-fav-course.html', {"course_list":course_list})


class MyMessageView(LoginRequiredMixin, View):
    """
    我的消息
    """
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation

        p = Paginator(all_message, 3, request=request)
        # 不是一个queryset对象，所以在模板中需要修改 {%for message in messages.object_list%}
        messages = p.page(page)

        return render(request, 'usercenter-message.html', {'messages':messages})


class IndexView(View):
    def get(self, request):
        all_banners = Banner.objects.order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {"all_banners":all_banners,
                                              "courses":courses,
                                              "banner_courses":banner_courses,
                                              "course_orgs":course_orgs})


def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html', {})
    response.status_code = 404
    return response


# coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
import json
from .tasks import send_register


def home(request):
    send_register.delay('baliang616@sina.com')

    data = list(Teacher.objects.values('name'))
    return HttpResponse(json.dumps(data), content_type='application/json')