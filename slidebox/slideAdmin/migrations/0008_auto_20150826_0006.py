# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('slideAdmin', '0007_auto_20150807_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalid',
            name='IDnumber',
            field=models.CharField(verbose_name='animal ID', max_length=10, validators=[django.core.validators.RegexValidator(regex='[a-z]{2}[0-9]{2,3}', message='Animal ID must consist of two sets of two letters and 1-3 numbers, e.g., gy6or113')]),
        ),
        migrations.AlterField(
            model_name='injection',
            name='anatTarget',
            field=models.ForeignKey(verbose_name='anatomical target', to='slideAdmin.anatAreas'),
        ),
        migrations.AlterField(
            model_name='injection',
            name='animalID',
            field=models.ForeignKey(verbose_name='animal ID', default=None, to='slideAdmin.animalID'),
        ),
        migrations.AlterField(
            model_name='injection',
            name='beakBarAngle',
            field=models.DecimalField(verbose_name='beak bar angle', max_digits=3, decimal_places=1),
        ),
        migrations.AlterField(
            model_name='injection',
            name='probeArmAngle',
            field=models.DecimalField(verbose_name='probe arm angle', max_digits=3, decimal_places=1),
        ),
    ]
