# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0019_auto_20150414_0552'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeMonitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('recipe', models.CharField(default=b'', max_length=100, blank=True)),
                ('device', models.ForeignKey(related_name='device_recipemonitor', to='BaseInfo.Device')),
                ('release', models.ForeignKey(related_name='release_recipemonitor', to='BaseInfo.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('device', models.ForeignKey(related_name='device_task', to='BaseInfo.Device')),
                ('release', models.ForeignKey(related_name='release_task', to='BaseInfo.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task', models.ForeignKey(related_name='task_taskrun', to='BaseInfo.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='recipemonitor',
            name='run',
            field=models.ForeignKey(related_name='taskrun_recipemonitor', default=1, blank=True, to='BaseInfo.TaskRun'),
            preserve_default=True,
        ),
    ]
