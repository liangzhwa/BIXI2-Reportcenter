# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0025_auto_20150415_0946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devicedeploy',
            old_name='bbcody',
            new_name='bbcode',
        ),
    ]
