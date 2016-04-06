# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0010_auto_20150318_0142'),
    ]

    operations = [
        migrations.CreateModel(
            name='KpiPriority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='kpi',
            name='kpipriority',
            field=models.ForeignKey(related_name='kpipriority_kpi', default=1, to='BaseInfo.KpiPriority'),
            preserve_default=True,
        ),
    ]
