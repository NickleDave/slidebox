# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('slideAdmin', '0004_auto_20150708_0015'),
    ]

    operations = [
        migrations.AddField(
            model_name='animalid',
            name='sectionsPerSlide',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], default=6),
        ),
    ]
