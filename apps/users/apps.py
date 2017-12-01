# coding:utf8
from __future__ import unicode_literals

from django.apps import AppConfig
"""
应用在后台管理页面中显示中文名字
"""


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = u'用户管理'
