# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slideAdmin', '0002_auto_20150707_2042'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='results',
            unique_together=set([]),
        ),
    ]
