# coding:utf8

from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher


class Course(models.Model):
    """
    课程
    """
    course_org = models.ForeignKey(CourseOrg, null=True, verbose_name=u'课程机构')
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=300, verbose_name=u"课程表述")
    detail = models.TextField(verbose_name=u'课程详情')
    degree = models.CharField(choices=(('cj', u'初级'), ('zj', u'中级'), ('gj','高级')), max_length=2, verbose_name=u'难度')
    learn_times = models.IntegerField(verbose_name='时长', default=0)
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    category = models.CharField(u'课程类别', default=u'培训', max_length=20)
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name=u"封面图", max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u"点击数")
    tag = models.CharField(u"课程标签", default="", max_length=10)
    teacher = models.ForeignKey(Teacher, null=True, blank=True, verbose_name=u'讲师')
    youneed_know = models.CharField(u'用户须知', default="", max_length=300)
    teacher_tell = models.CharField(u'老师告诉', default="", max_length=300)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    def chapter_num(self):
        """
        获取章节数
        :return:
        """
        return self.lesson_set.all().count()

    def user_courses(self):
        """
        学习用户
        :return:
        """
        return self.usercourse_set.all()[:5]

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class Lesson(models.Model):
    """
    章节
    """
    course = models.ForeignKey(Course, verbose_name=u'课程章节')
    name = models.CharField(max_length=10, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    def get_video(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u"章节")
    name = models.CharField(max_length=10, verbose_name=u'视频名')
    url = models.URLField(u'地址', default="", max_length=30)
    learn_times = models.IntegerField(verbose_name='时长', default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    download = models.FileField(upload_to='course/resource/%Y/%m', max_length=100, verbose_name=u'资源文件')
    name = models.CharField(max_length=10, verbose_name=u'资源名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"课程资源"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

