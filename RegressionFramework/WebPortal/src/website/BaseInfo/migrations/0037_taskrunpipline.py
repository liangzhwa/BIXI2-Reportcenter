# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0036_auto_20150526_0526'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskRunPipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateField(default=datetime.datetime.now, null=True, blank=True)),
                ('run', models.ForeignKey(related_name='taskrun_taskrunpipline', default=1, blank=True, to='BaseInfo.TaskRun')),
                ('status', models.ForeignKey(related_name='taskrunstatus_taskrunpipline', default=None, to='BaseInfo.TaskRunStatus')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
