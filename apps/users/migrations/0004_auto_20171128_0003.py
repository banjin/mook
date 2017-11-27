# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2017-11-28 00:03
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20171125_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='\u53d1\u9001\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='emailverifyrecord',
            name='send_type',
            field=models.CharField(choices=[(b'register', '\u6ce8\u518c'), (b'forget', '\u627e\u56de\u5bc6\u7801')], max_length=20, verbose_name='\u9a8c\u8bc1\u7801\u7c7b\u578b'),
        ),
    ]
