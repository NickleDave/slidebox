# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='anatAreas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('areaName', models.CharField(verbose_name='anatomical area name', max_length=100)),
                ('abbreviation', models.CharField(max_length=5)),
            ],
            options={
                'verbose_name': 'anatomical area',
            },
        ),
        migrations.CreateModel(
            name='animalID',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('IDnumber', models.CharField(verbose_name='animal ID', max_length=10)),
                ('surgeryDate', models.DateField(verbose_name='date of surgery')),
                ('perfusionDate', models.DateField(verbose_name='date of perfusion')),
                ('surgeryNotebook', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('surgeryNotebookPage', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('sectionDate', models.DateField()),
                ('sectionPlane', models.CharField(choices=[('PS', 'Parasagittal'), ('CO', 'Coronal'), ('HO', 'Horizontal')], max_length=2, default='PS')),
                ('sectionThickness', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
            ],
        ),
        migrations.CreateModel(
            name='channelTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('channel', models.CharField(verbose_name='channel name', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='injection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('current', models.IntegerField(blank=True, verbose_name='current in uA', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('seconds_on', models.DecimalField(blank=True, verbose_name='seconds on', null=True, max_digits=3, decimal_places=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('seconds_off', models.DecimalField(blank=True, verbose_name='seconds off', null=True, max_digits=3, decimal_places=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('nl_per_inject', models.DecimalField(blank=True, verbose_name='nanoliters per inject', null=True, max_digits=3, decimal_places=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('number_injects', models.IntegerField(blank=True, verbose_name='number of times "Inject" was pressed', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('sec_bt_injects', models.IntegerField(blank=True, verbose_name='seconds waited between pressing "Inject"', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('APcoord', models.DecimalField(verbose_name='anterior-posterior co-ordinate', max_digits=3, decimal_places=2)),
                ('LMcoord', models.DecimalField(verbose_name='lateral-medial co-ordinate', max_digits=3, decimal_places=2)),
                ('DVcoord', models.DecimalField(verbose_name='dorsal-ventral co-ordinate', max_digits=3, decimal_places=2)),
                ('beakBarAngle', models.DecimalField(max_digits=3, decimal_places=1)),
                ('probeArmAngle', models.DecimalField(max_digits=3, decimal_places=1)),
                ('comments', models.TextField(blank=True)),
                ('anatTarget', models.ForeignKey(to='slideAdmin.anatAreas')),
                ('animalID', models.ForeignKey(to='slideAdmin.animalID', default=None)),
            ],
        ),
        migrations.CreateModel(
            name='injectMethods',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('method', models.CharField(verbose_name='injection method', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='results',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('slideNum', models.IntegerField(verbose_name='slide number', validators=[django.core.validators.MinValueValidator(1)])),
                ('sectionNum', models.IntegerField(verbose_name='section number', validators=[django.core.validators.MinValueValidator(1)])),
                ('anatArea', models.ForeignKey(to='slideAdmin.anatAreas')),
                ('animalID', models.ForeignKey(to='slideAdmin.animalID')),
                ('channel', models.ForeignKey(to='slideAdmin.channelTypes')),
            ],
        ),
        migrations.CreateModel(
            name='resultTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('result', models.CharField(verbose_name='result type', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='solvents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nameOfSolvent', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'solvent',
            },
        ),
        migrations.CreateModel(
            name='tracers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nameOfTracer', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'tracer',
            },
        ),
        migrations.CreateModel(
            name='tracerTypes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('percentDilution', models.DecimalField(max_digits=5, decimal_places=2)),
                ('solventName', models.ForeignKey(to='slideAdmin.solvents')),
                ('tracerName', models.ForeignKey(to='slideAdmin.tracers')),
            ],
            options={
                'verbose_name': 'tracer, percent solution, and solvent',
            },
        ),
        migrations.AddField(
            model_name='results',
            name='result',
            field=models.ForeignKey(to='slideAdmin.resultTypes'),
        ),
        migrations.AddField(
            model_name='injection',
            name='injectionMethod',
            field=models.ForeignKey(to='slideAdmin.injectMethods'),
        ),
        migrations.AddField(
            model_name='injection',
            name='tracer',
            field=models.ForeignKey(to='slideAdmin.tracerTypes'),
        ),
        migrations.AlterUniqueTogether(
            name='results',
            unique_together=set([('animalID', 'slideNum', 'sectionNum', 'result', 'anatArea', 'channel')]),
        ),
    ]
