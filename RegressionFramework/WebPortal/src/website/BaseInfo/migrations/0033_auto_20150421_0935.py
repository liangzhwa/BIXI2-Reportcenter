# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0032_auto_20150421_0928'),
    ]

    operations = [
        migrations.RenameField(
            model_name='releasetype',
            old_name='brachpath',
            new_name='branchpath',
        ),
    ]
