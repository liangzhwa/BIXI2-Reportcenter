# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0009_auto_20150318_0137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='largeisbetter',
            field=models.NullBooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kpi',
            name='unit',
            field=models.ForeignKey(related_name='unit_kpi', default=2, to='BaseInfo.Unit'),
            preserve_default=True,
        ),
    ]
