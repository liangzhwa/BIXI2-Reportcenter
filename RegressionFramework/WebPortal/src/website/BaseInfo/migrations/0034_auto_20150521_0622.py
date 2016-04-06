# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0033_auto_20150421_0935'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestResultComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(blank=True)),
                ('remark', models.TextField(blank=True)),
                ('isavailable', models.NullBooleanField(default=True)),
                ('device', models.ForeignKey(related_name='device_testresultcomment', to='BaseInfo.Device')),
                ('kpi', models.ForeignKey(related_name='kpi_testresultcomment', to='BaseInfo.KPI')),
                ('release', models.ForeignKey(related_name='release_testresultcomment', to='BaseInfo.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='testresult',
            name='rankindex',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
