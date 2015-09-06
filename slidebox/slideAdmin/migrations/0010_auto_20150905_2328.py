# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slideAdmin', '0009_auto_20150826_0833'),
    ]

    operations = [
        migrations.AlterField(
            model_name='injection',
            name='injectionMethod',
            field=models.ForeignKey(verbose_name='injection method', to='slideAdmin.injectMethods'),
        ),
    ]
