# coding:utf-8
import xadmin

from .models import UserAsk, CourseComment, UserFavorite,UserMessage, UserCourse


class UserAskAdmin(object):
    list_display = ('name', 'mobile', 'course_name','add_time')
    search_fields = ('name', 'mobile', 'course_name')
    list_filter = ('name', 'mobile', 'course_name','add_time')


class CourseCommentAdmin(object):
    list_display = ('user', 'course', 'comment', 'add_time')
    search_fields = ('user', 'course', 'comment',)
    list_filter = ('user', 'course', 'comment', 'add_time')


class UserFavoriteAdmin(object):
    list_display = ('user', 'fav_id', 'fav_type', 'add_time')
    search_fields = ('user', 'fav_id', 'fav_type',)
    list_filter = ('user', 'fav_id', 'fav_type', 'add_time')


class UserMessageAdmin(object):
    list_display = ('user', 'message', 'has_read', 'add_time')
    search_fields = ('user', 'message', 'has_read')
    list_filter = ('user', 'message', 'has_read', 'add_time')


class UserCourseAdmin(object):
    # def get_name(self, obj):
    #     return obj.user.username
    #
    # get_name.admin_order_field = 'user'  # Allows column order sorting
    # get_name.short_description = 'User Name'
    #
    # list_display = ('get_name', 'course', 'add_time')
    # search_fields = ('get_name', 'course')
    # list_filter = ('get_name', 'course', 'add_time')
    list_display = ('user', 'course', 'add_time')
    search_fields = ('user', 'course')
    list_filter = ('user', 'course', 'add_time')

xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)

