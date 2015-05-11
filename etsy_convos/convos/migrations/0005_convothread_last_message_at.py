# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convos', '0004_auto_20150511_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='convothread',
            name='last_message_at',
            field=models.DateTimeField(null=True, verbose_name='Last message at', blank=True),
        ),
    ]
