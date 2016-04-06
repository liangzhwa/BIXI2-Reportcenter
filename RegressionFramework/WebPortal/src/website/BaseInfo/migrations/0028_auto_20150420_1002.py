# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0027_testresultfrom'),
    ]

    operations = [
        migrations.AddField(
            model_name='testresult',
            name='datafrom',
            field=models.ForeignKey(related_name='testresultfrom_testresult', default=1, to='BaseInfo.TestResultFrom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='testresult',
            name='isavailable',
            field=models.NullBooleanField(default=True),
            preserve_default=True,
        ),
    ]
