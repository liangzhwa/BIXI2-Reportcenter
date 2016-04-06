# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0015_auto_20150319_0219'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReleaseType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='release',
            name='releasetype',
            field=models.ForeignKey(related_name='releasetype_release', default=None, to='BaseInfo.ReleaseType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='testresult',
            name='jobid',
            field=models.CharField(default=b'', max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
