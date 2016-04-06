# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BaseInfo', '0024_recipemonitor_failecount'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeviceDeploy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip', models.CharField(max_length=100)),
                ('sn', models.CharField(max_length=100)),
                ('bbcody', models.CharField(max_length=100)),
                ('site', models.CharField(max_length=100)),
                ('room', models.CharField(max_length=100)),
                ('device', models.ForeignKey(related_name='device_devicedeploy', to='BaseInfo.Device')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PNPRole',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PNPRoleKPI',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kpi', models.ForeignKey(related_name='kpi_pnprolekpi', to='BaseInfo.KPI')),
                ('pnprole', models.ForeignKey(related_name='pnprole_pnprolekpi', to='BaseInfo.PNPRole')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='devicedeploy',
            name='pnprole',
            field=models.ForeignKey(related_name='pnprole_devicedeploy', to='BaseInfo.PNPRole'),
            preserve_default=True,
        ),
    ]
