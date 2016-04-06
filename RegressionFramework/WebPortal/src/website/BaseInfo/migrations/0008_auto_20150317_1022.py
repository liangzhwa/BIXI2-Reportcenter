# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0007_auto_20150317_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='kpitype',
            field=models.ForeignKey(related_name='kpitype_kpi', default=2, to='BaseInfo.KpiType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kpi',
            name='largeisbetter',
            field=models.NullBooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kpi',
            name='unit',
            field=models.ForeignKey(related_name='unit_kpi', default=4, to='BaseInfo.Unit'),
            preserve_default=True,
        ),
    ]
