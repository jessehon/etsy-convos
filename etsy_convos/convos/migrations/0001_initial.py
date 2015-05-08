# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Convo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('body', models.TextField()),
                ('sender_read_at', models.DateTimeField(null=True, verbose_name='Sender read at', blank=True)),
                ('recipient_read_at', models.DateTimeField(null=True, verbose_name='Recipient read at', blank=True)),
                ('created_at', django_extensions.db.fields.CreationDateTimeField(default=django.utils.timezone.now, verbose_name='Created at', editable=False, blank=True)),
                ('recipient', models.ForeignKey(related_name='convos_received', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='convos_sent', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ConvoThread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(max_length=140)),
            ],
        ),
        migrations.AddField(
            model_name='convo',
            name='thread',
            field=models.ForeignKey(to='convos.ConvoThread'),
        ),
    ]
