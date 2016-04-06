# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0012_kpi_margin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kpi',
            name='margin',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
