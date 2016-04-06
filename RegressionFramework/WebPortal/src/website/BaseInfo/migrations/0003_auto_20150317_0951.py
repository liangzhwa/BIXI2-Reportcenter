# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0002_auto_20150317_0940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='release',
            name='pre',
            field=models.ForeignKey(related_name='release_release', to='BaseInfo.Release', null=True),
            preserve_default=True,
        ),
    ]
