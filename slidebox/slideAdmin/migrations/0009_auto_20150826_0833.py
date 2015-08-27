# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('slideAdmin', '0008_auto_20150826_0006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='animalid',
            name='sectionDate',
            field=models.DateField(verbose_name='sectioning data'),
        ),
        migrations.AlterField(
            model_name='animalid',
            name='sectionPlane',
            field=models.CharField(max_length=2, choices=[('PS', 'Parasagittal'), ('CO', 'Coronal'), ('HO', 'Horizontal')], verbose_name='plane of section', default='PS'),
        ),
        migrations.AlterField(
            model_name='animalid',
            name='sectionThickness',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='section thickness'),
        ),
        migrations.AlterField(
            model_name='animalid',
            name='sectionsPerSlide',
            field=models.IntegerField(default=6, validators=[django.core.validators.MinValueValidator(1)], verbose_name='sections per slide'),
        ),
        migrations.AlterField(
            model_name='animalid',
            name='surgeryNotebook',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='surgery notebook'),
        ),
        migrations.AlterField(
            model_name='animalid',
            name='surgeryNotebookPage',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='surgery notebook page'),
        ),
    ]
