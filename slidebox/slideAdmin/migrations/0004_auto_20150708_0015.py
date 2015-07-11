# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slideAdmin', '0003_auto_20150708_0014'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='injection',
            unique_together=set([]),
        ),
        migrations.AlterUniqueTogether(
            name='results',
            unique_together=set([('animalID', 'slideNum', 'sectionNum', 'result', 'anatArea', 'channel')]),
        ),
    ]
