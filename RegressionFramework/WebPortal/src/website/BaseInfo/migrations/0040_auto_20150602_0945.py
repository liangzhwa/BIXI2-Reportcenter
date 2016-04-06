# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0039_taskrunpipline_completekpinum'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testresult',
            old_name='rankindex',
            new_name='runindex',
        ),
    ]
