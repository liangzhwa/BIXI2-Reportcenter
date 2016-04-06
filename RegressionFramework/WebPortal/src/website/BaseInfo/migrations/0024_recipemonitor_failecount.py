# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0023_recipemonitor_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipemonitor',
            name='failecount',
            field=models.CharField(default=0, max_length=100),
            preserve_default=True,
        ),
    ]
