# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0044_auto_20150625_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'', max_length=10, blank=True)),
                ('devicedeploy', models.ForeignKey(related_name='devicedeploy_plantask', default=1, to='BaseInfo.DeviceDeploy')),
                ('releasetype', models.ForeignKey(related_name='releasetype_plantask', default=1, to='BaseInfo.ReleaseType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlanTaskRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.CharField(default=b'', max_length=100, blank=True)),
                ('jobid', models.CharField(default=b'', max_length=100, blank=True)),
                ('finishedkpinum', models.IntegerField(default=0, blank=True)),
                ('totalkpinum', models.IntegerField(default=0, blank=True)),
                ('totalestimatetime', models.IntegerField(default=0, blank=True)),
                ('plantask', models.ForeignKey(related_name='plantask_taskrun', to='BaseInfo.PlanTask')),
                ('status', models.ForeignKey(related_name='taskrunstatus_plantaskrun', default=None, to='BaseInfo.TaskRunStatus')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlanTaskRunPipline',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)),
                ('completekpinum', models.IntegerField(default=0, blank=True)),
                ('run', models.ForeignKey(related_name='plantaskrun_plantaskrunpipline', default=1, blank=True, to='BaseInfo.PlanTaskRun')),
                ('status', models.ForeignKey(related_name='taskrunstatus_plantaskrunpipline', default=None, to='BaseInfo.TaskRunStatus')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='releasepullrequest',
            name='pullrequest',
        ),
        migrations.RemoveField(
            model_name='releasepullrequest',
            name='release',
        ),
        migrations.DeleteModel(
            name='ReleasePullRequest',
        ),
        migrations.RemoveField(
            model_name='task',
            name='devicedeploy',
        ),
        migrations.RemoveField(
            model_name='task',
            name='releasetype',
        ),
        migrations.RemoveField(
            model_name='taskrun',
            name='status',
        ),
        migrations.RemoveField(
            model_name='taskrun',
            name='task',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
        migrations.RemoveField(
            model_name='taskrunpipline',
            name='run',
        ),
        migrations.RemoveField(
            model_name='taskrunpipline',
            name='status',
        ),
        migrations.DeleteModel(
            name='TaskRunPipline',
        ),
        migrations.RenameField(
            model_name='pullrequest',
            old_name='ingrationurl',
            new_name='jiraurl',
        ),
        migrations.RemoveField(
            model_name='bisectresult',
            name='pullrequest',
        ),
        migrations.RemoveField(
            model_name='bisecttask',
            name='devicedeploy',
        ),
        migrations.RemoveField(
            model_name='bisecttask',
            name='release',
        ),
        migrations.RemoveField(
            model_name='pullrequest',
            name='preingration',
        ),
        migrations.RemoveField(
            model_name='pullrequest',
            name='pullurl',
        ),
        migrations.AddField(
            model_name='bisectresult',
            name='preimage',
            field=models.ForeignKey(related_name='preimage_bisectresult', to='BaseInfo.PreImage', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bisecttask',
            name='plantaskrun',
            field=models.ForeignKey(related_name='plantaskrun_bisecttask', to='BaseInfo.PlanTaskRun', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='preimage',
            name='downloadpath',
            field=models.CharField(default=b'', max_length=1024),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='preimage',
            name='localpath',
            field=models.CharField(default=b'', max_length=1024),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='preimage',
            name='release',
            field=models.ForeignKey(related_name='release_preimage', default=None, to='BaseInfo.Release'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pullrequest',
            name='preimage',
            field=models.ForeignKey(related_name='preimage_pullrequest', to='BaseInfo.PreImage', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='pullrequest',
            name='release',
            field=models.ForeignKey(related_name='release_pullrequest', to='BaseInfo.Release', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='recipemonitor',
            name='run',
            field=models.ForeignKey(related_name='plantaskrun_recipemonitor', default=1, blank=True, to='BaseInfo.PlanTaskRun'),
            preserve_default=True,
        ),
        migrations.DeleteModel(
            name='TaskRun',
        ),
    ]
