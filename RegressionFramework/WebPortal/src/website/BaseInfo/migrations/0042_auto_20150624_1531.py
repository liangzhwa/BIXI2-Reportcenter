# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0041_target_rsd'),
    ]

    operations = [
        migrations.CreateModel(
            name='BisectTask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'', max_length=10, blank=True)),
                ('devicedeploy', models.ForeignKey(related_name='devicedeploy_bisecttask', default=1, to='BaseInfo.DeviceDeploy')),
                ('release', models.ForeignKey(related_name='release_bisecttask', to='BaseInfo.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BisectTaskKpi',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bisecttask', models.ForeignKey(related_name='bisecttask_bisecttaskkpi', to='BaseInfo.BisectTask')),
                ('kpi', models.ForeignKey(related_name='kpi_bisecttaskkpi', to='BaseInfo.KPI')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BisectTaskRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jobid', models.CharField(default=b'', max_length=100, blank=True)),
                ('finishedkpinum', models.IntegerField(default=0, blank=True)),
                ('totalkpinum', models.IntegerField(default=0, blank=True)),
                ('totalestimatetime', models.IntegerField(default=0, blank=True)),
                ('bisecttask', models.ForeignKey(related_name='bisecttask_bisecttaskrun', to='BaseInfo.BisectTask')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PreImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('isdownloaded', models.NullBooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='bisecttaskrun',
            name='preimage',
            field=models.ForeignKey(related_name='preimage_bisecttaskrun', to='BaseInfo.PreImage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bisecttaskrun',
            name='status',
            field=models.ForeignKey(related_name='taskrunstatus_bisecttaskrun', default=None, to='BaseInfo.TaskRunStatus'),
            preserve_default=True,
        ),
    ]
