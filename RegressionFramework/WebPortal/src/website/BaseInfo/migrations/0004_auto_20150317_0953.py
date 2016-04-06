# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0003_auto_20150317_0951'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='pre',
            field=models.ForeignKey(related_name='release_release', blank=True, to='BaseInfo.Release', null=True),
            preserve_default=True,
        ),
    ]
