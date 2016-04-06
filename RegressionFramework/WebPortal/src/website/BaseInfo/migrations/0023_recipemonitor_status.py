# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0022_auto_20150415_0139'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipemonitor',
            name='status',
            field=models.CharField(default=0, max_length=1),
            preserve_default=True,
        ),
    ]
