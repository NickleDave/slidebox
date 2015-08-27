# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('slideAdmin', '0006_auto_20150805_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalid',
            name='IDnumber',
            field=models.CharField(validators=[django.core.validators.RegexValidator(regex='[a-z]{2}[0-9]{2,3}', message='Animal ID must consist of two letters followed by 2-3 numbers')], verbose_name='animal ID', max_length=10),
        ),
    ]
