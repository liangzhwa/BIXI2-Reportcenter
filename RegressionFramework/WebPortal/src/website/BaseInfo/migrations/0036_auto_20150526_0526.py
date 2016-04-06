# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0035_auto_20150526_0516'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskrun',
            name='finishedkpinum',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskrun',
            name='totalestimatetime',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taskrun',
            name='totalkpinum',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
