# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-04-04 04:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moles', '0009_consentdoc_original_filename'),
    ]

    operations = [
        migrations.AddField(
            model_name='moleimage',
            name='study',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='moles.Study', verbose_name='Study'),
        ),
    ]