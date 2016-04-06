# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0037_taskrunpipline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskrunpipline',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, blank=True),
            preserve_default=True,
        ),
    ]
