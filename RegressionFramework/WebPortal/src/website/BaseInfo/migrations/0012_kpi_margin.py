# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0011_auto_20150318_0558'),
    ]

    operations = [
        migrations.AddField(
            model_name='kpi',
            name='margin',
            field=models.DecimalField(default=1, max_digits=4, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
