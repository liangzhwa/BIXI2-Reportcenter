# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0038_auto_20150527_0507'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskrunpipline',
            name='completekpinum',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
