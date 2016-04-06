# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0016_auto_20150325_0231'),
    ]

    operations = [
        migrations.CreateModel(
            name='BisectResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('jobid', models.CharField(default=b'', max_length=100, blank=True)),
                ('value', models.DecimalField(max_digits=10, decimal_places=2)),
                ('remark', models.TextField(blank=True)),
                ('baserelease', models.ForeignKey(related_name='baserelease_bisectresult', to='BaseInfo.Release')),
                ('device', models.ForeignKey(related_name='device_bisectresult', to='BaseInfo.Device')),
                ('kpi', models.ForeignKey(related_name='kpi_bisectresult', to='BaseInfo.KPI')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PullRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('pullurl', models.CharField(max_length=500)),
                ('preingration', models.CharField(max_length=100)),
                ('ingrationurl', models.CharField(max_length=500)),
                ('remark', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReleasePullRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pullrequest', models.ForeignKey(related_name='device_releasepullrequest', to='BaseInfo.PullRequest')),
                ('release', models.ForeignKey(related_name='release_releasepullrequest', to='BaseInfo.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='bisect',
            name='nextrelease',
        ),
        migrations.RemoveField(
            model_name='bisect',
            name='prerelease',
        ),
        migrations.DeleteModel(
            name='Bisect',
        ),
        migrations.AddField(
            model_name='bisectresult',
            name='pullrequest',
            field=models.ForeignKey(related_name='device_bisectresult', to='BaseInfo.PullRequest'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bisectresult',
            name='targetrelease',
            field=models.ForeignKey(related_name='targetrelease_bisectresult', to='BaseInfo.Release'),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='kpi',
            name='margin',
        ),
        migrations.RemoveField(
            model_name='target',
            name='value',
        ),
        migrations.AddField(
            model_name='target',
            name='margin',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='target',
            name='regthrethold1',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='target',
            name='regthrethold2',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='target',
            name='regthrethold3',
            field=models.DecimalField(default=0, max_digits=3, decimal_places=2, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='target',
            name='target',
            field=models.DecimalField(default=0, max_digits=10, decimal_places=2, blank=True),
            preserve_default=True,
        ),
    ]
