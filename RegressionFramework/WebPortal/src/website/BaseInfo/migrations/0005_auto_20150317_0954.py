# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0004_auto_20150317_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='releasedate',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
