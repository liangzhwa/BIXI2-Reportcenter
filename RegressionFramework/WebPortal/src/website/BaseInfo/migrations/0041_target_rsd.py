# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0040_auto_20150602_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='target',
            name='rsd',
            field=models.DecimalField(default=10, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
