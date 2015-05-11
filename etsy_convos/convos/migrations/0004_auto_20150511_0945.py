# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convos', '0003_auto_20150511_0440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convomessage',
            name='body',
            field=models.CharField(max_length=64000),
        ),
    ]
