# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-22 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testmanagement', '0003_auto_20161122_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testexecution',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, b'UNEXECUTED'), (1, b'PASSED'), (2, b'FAILED'), (3, b'BLOCKED')], default=0),
        ),
    ]
