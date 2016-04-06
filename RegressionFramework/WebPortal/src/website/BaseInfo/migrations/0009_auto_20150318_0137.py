# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0008_auto_20150317_1022'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='kpitype',
            field=models.ForeignKey(related_name='kpitype_kpi', default=1, to='BaseInfo.KpiType'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kpi',
            name='unit',
            field=models.ForeignKey(related_name='unit_kpi', default=1, to='BaseInfo.Unit'),
            preserve_default=True,
        ),
    ]
