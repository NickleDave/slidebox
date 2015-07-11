# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slideAdmin', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='injection',
            unique_together=set([('animalID', 'anatTarget', 'tracer', 'injectionMethod', 'current', 'seconds_on', 'seconds_off', 'nl_per_inject', 'number_injects', 'sec_bt_injects', 'APcoord', 'LMcoord', 'DVcoord', 'beakBarAngle', 'probeArmAngle', 'comments')]),
        ),
    ]
