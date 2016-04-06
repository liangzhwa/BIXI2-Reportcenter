# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0031_auto_20150421_0551'),
    ]

    operations = [
        migrations.AddField(
            model_name='releasetype',
            name='brachpath',
            field=models.CharField(default=b'', max_length=500),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taskrun',
            name='status',
            field=models.ForeignKey(related_name='taskrunstatus_taskrun', default=None, to='BaseInfo.TaskRunStatus'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taskrun',
            name='task',
            field=models.ForeignKey(related_name='task_taskrun', to='BaseInfo.Task'),
            preserve_default=True,
        ),
    ]
