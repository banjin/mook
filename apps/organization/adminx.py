# coding:utf-8
import xadmin

from .models import CityDict, CourseOrg, Teacher


class CityDictAdmin(object):
    list_display = ('desc', 'name', 'add_time')
    search_fields = ('desc', 'name')
    list_filter = ('desc', 'name', 'add_time')


class CourseOrgAdmin(object):
    list_display = ('name', 'desc', 'click_num', 'address', 'city', 'fav_nums', 'image', 'add_time')
    search_fields = ('name', 'desc', 'click_num', 'address', 'city', 'fav_nums', 'image')
    list_filter = ('name', 'desc', 'click_num', 'address', 'city', 'fav_nums', 'image', 'add_time')


class TeacherAdmin(object):
    list_display = ('org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_nums', 'add_time')
    search_fields = ('org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_nums')
    list_filter = ('org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_nums', 'add_time')


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
