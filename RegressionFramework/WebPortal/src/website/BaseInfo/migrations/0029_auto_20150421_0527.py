# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0028_auto_20150420_1002'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskRunStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'', max_length=100, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='task',
            name='device',
        ),
        migrations.RemoveField(
            model_name='task',
            name='release',
        ),
        migrations.AddField(
            model_name='releasetype',
            name='gituri',
            field=models.CharField(default=b'', max_length=500),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='releasetype',
            name='ismonitor',
            field=models.NullBooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='devicedeploy',
            field=models.ForeignKey(related_name='devicedeploy_task', default=1, to='BaseInfo.DeviceDeploy'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='releasetype',
            field=models.ForeignKey(related_name='releasetype_task', default=1, to='BaseInfo.ReleaseType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(default=b'', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskrun',
            name='image',
            field=models.CharField(default=b'', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskrun',
            name='jobid',
            field=models.CharField(default=b'', max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskrun',
            name='runstarttime',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskrun',
            name='starttime',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskrun',
            name='status',
            field=models.ForeignKey(related_name='taskrunstatus_taskrun', default=1, to='BaseInfo.TaskRunStatus'),
            preserve_default=True,
        ),
    ]
