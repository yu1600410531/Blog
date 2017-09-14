# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fire', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='profile',
            field=models.CharField(default='', max_length=256, verbose_name='profile'),
        ),
    ]
