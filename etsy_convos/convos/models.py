# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

class ConvoThread(models.Model):
    """
    Model used to group related messages together
    """
    subject = models.CharField(max_length=140)

class Convo(models.Model):
    """
    Model that houses the main body of the message
    """
    thread = models.ForeignKey(ConvoThread)
    body = models.TextField()
    sender = models.ForeignKey(User, related_name='convos_sent')
    sender_read_at = models.DateTimeField(_("Sender read at"), blank=True, null=True)
    recipient = models.ForeignKey(User, related_name='convos_received')
    recipient_read_at = models.DateTimeField(_("Recipient read at"), blank=True, null=True)

    created_at = CreationDateTimeField(_("Created at"), blank=True)

    @property
    def excerpt(self):
        return self.body[:49]+'...' if len(self.body) > 50 else self.body
