# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0018_auto_20150401_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpi',
            name='key',
            field=models.TextField(default=b'', max_length=500, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kpi',
            name='summary',
            field=models.TextField(default=b'', max_length=500, blank=True),
            preserve_default=True,
        ),
    ]
