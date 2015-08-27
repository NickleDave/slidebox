# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('slideAdmin', '0005_animalid_sectionsperslide'),
    ]

    operations = [
        migrations.AddField(
            model_name='injection',
            name='duration',
            field=models.IntegerField(blank=True, verbose_name='duration (minutes)', validators=[django.core.validators.MinValueValidator(0)], null=True),
        ),
        migrations.AddField(
            model_name='injection',
            name='time_waited_after_injection',
            field=models.IntegerField(blank=True, verbose_name='Time waited after injection (minutes)', validators=[django.core.validators.MinValueValidator(0)], null=True),
        ),
    ]
