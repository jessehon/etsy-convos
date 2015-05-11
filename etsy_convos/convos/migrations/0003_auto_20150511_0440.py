# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convos', '0002_auto_20150510_0625'),
    ]

    operations = [
        migrations.AddField(
            model_name='convomessage',
            name='recipient_deleted_at',
            field=models.DateTimeField(null=True, verbose_name='Recipient deleted at', blank=True),
        ),
        migrations.AddField(
            model_name='convomessage',
            name='sender_deleted_at',
            field=models.DateTimeField(null=True, verbose_name='Sender deleted at', blank=True),
        ),
    ]
