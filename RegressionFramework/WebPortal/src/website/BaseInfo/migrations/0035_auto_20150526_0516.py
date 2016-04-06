# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0034_auto_20150521_0622'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskrun',
            name='runstarttime',
        ),
        migrations.RemoveField(
            model_name='taskrun',
            name='starttime',
        ),
    ]
