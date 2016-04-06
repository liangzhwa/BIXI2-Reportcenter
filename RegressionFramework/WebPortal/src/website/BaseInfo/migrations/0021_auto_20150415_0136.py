# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0020_auto_20150414_1017'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipemonitor',
            name='run',
            field=models.ForeignKey(related_name='taskrun_recipemonitor', blank=True, to='BaseInfo.TaskRun'),
            preserve_default=True,
        ),
    ]
