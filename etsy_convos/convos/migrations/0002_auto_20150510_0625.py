# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('convos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='convomessage',
            name='recipient_read_at',
        ),
        migrations.RemoveField(
            model_name='convomessage',
            name='sender_read_at',
        ),
        migrations.AddField(
            model_name='convomessage',
            name='recipient_read',
            field=models.BooleanField(default=False, verbose_name='Recipient read'),
        ),
        migrations.AddField(
            model_name='convomessage',
            name='sender_read',
            field=models.BooleanField(default=False, verbose_name='Sender read'),
        ),
    ]
