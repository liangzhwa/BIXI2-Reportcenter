# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0021_auto_20150415_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipemonitor',
            name='run',
            field=models.ForeignKey(related_name='taskrun_recipemonitor', default=1, blank=True, to='BaseInfo.TaskRun'),
            preserve_default=True,
        ),
    ]
