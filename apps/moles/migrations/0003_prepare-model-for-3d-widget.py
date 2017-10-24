# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-24 03:17
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.core.files.storage


def forwards_func(apps, schema_editor):
    Mole = apps.get_model("moles", "Mole")
    PatientAnatomicalSite = apps.get_model("moles", "PatientAnatomicalSite")

    for mole in Mole.objects.all().iterator():
        mole.position_info = {
            'x': mole.position_x,
            'y': mole.position_y,
        }
        mole.patient_anatomical_site = PatientAnatomicalSite.objects.filter(
            patient=mole.patient, anatomical_site=mole.anatomical_site).first()
        mole.save()


def reverse_func(apps, schema_editor):
    Mole = apps.get_model("moles", "Mole")

    for mole in Mole.objects.all().iterator():
        mole.position_x = mole.position_info['x']
        mole.position_y = mole.position_info['y']
        mole.save()


class Migration(migrations.Migration):

    dependencies = [('moles', '0002_setup-anatomical-site'), ]

    operations = [
        migrations.RunSQL('SET CONSTRAINTS ALL IMMEDIATE',
                          reverse_sql=migrations.RunSQL.noop),
        migrations.AddField(
            model_name='mole',
            name='patient_anatomical_site',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='moles.PatientAnatomicalSite',
                verbose_name='Patient anatomical site'), ),
        migrations.AddField(
            model_name='mole',
            name='position_info',
            field=django.contrib.postgres.fields.jsonb.JSONField(
                default={}, verbose_name='Mole position information'),
            preserve_default=False, ),
        migrations.RunPython(forwards_func, reverse_func),
        migrations.RemoveField(
            model_name='mole',
            name='position_x', ),
        migrations.RemoveField(
            model_name='mole',
            name='position_y', ),
        migrations.RunSQL('SET CONSTRAINTS ALL IMMEDIATE',
                          reverse_sql=migrations.RunSQL.noop),
    ]