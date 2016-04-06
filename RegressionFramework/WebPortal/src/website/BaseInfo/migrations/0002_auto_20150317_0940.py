# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bisect',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remark', models.TextField(blank=True)),
                ('nextrelease', models.ForeignKey(related_name='nextrelease_bisect', to='BaseInfo.Release')),
                ('prerelease', models.ForeignKey(related_name='prerelease_bisect', to='BaseInfo.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='KpiDomain',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.DecimalField(max_digits=4, decimal_places=2)),
                ('device', models.ForeignKey(related_name='device_target', to='BaseInfo.Device')),
                ('kpi', models.ForeignKey(related_name='kpi_target', to='BaseInfo.KPI')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TestResult',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('score', models.DecimalField(max_digits=4, decimal_places=2)),
                ('remark', models.TextField(blank=True)),
                ('device', models.ForeignKey(related_name='device_testresult', to='BaseInfo.Device')),
                ('kpi', models.ForeignKey(related_name='kpi_testresult', to='BaseInfo.KPI')),
                ('release', models.ForeignKey(related_name='release_testresult', to='BaseInfo.Release')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameModel(
            old_name='Component',
            new_name='Domain',
        ),
        migrations.AddField(
            model_name='kpidomain',
            name='domain',
            field=models.ForeignKey(related_name='domain_Kpidomain', to='BaseInfo.Domain'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='kpidomain',
            name='kpi',
            field=models.ForeignKey(related_name='kpi_Kpidomain', to='BaseInfo.KPI'),
            preserve_default=True,
        ),
        migrations.RenameField(
            model_name='kpi',
            old_name='name',
            new_name='showname',
        ),
        migrations.RenameField(
            model_name='kpi',
            old_name='scoretype',
            new_name='unit',
        ),
        migrations.RemoveField(
            model_name='kpi',
            name='component',
        ),
        migrations.RemoveField(
            model_name='kpi',
            name='kpisubtype',
        ),
        migrations.DeleteModel(
            name='KpiSubType',
        ),
        migrations.AddField(
            model_name='device',
            name='platform',
            field=models.ForeignKey(related_name='platform_device', default=1, to='BaseInfo.PlatForm'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kpi',
            name='testcasename',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='release',
            name='pre',
            field=models.ForeignKey(related_name='release_release', default=None, blank=True, to='BaseInfo.Release'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='release',
            name='remark',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='intelno',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='remark',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='device',
            name='sn',
            field=models.CharField(max_length=100, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kpi',
            name='largeisbetter',
            field=models.NullBooleanField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='kpi',
            name='remark',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='release',
            name='releasedate',
            field=models.DateField(blank=True),
            preserve_default=True,
        ),
    ]
