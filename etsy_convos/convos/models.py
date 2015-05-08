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

    def get_last_message(self):
        return self.convomessages.last()

class ConvoMessage(models.Model):
    """
    Model that houses the main body of the message
    """
    thread = models.ForeignKey(ConvoThread, related_name='convomessages')
    body = models.TextField()
    sender = models.ForeignKey(User, related_name='convomessages_sent')
    sender_read_at = models.DateTimeField(_("Sender read at"), blank=True, null=True)
    recipient = models.ForeignKey(User, related_name='convomessages_received')
    recipient_read_at = models.DateTimeField(_("Recipient read at"), blank=True, null=True)

    created_at = CreationDateTimeField(_("Created at"), blank=True)

    @property
    def body_excerpt(self):
        return self.body[:49]+'...' if len(self.body) > 50 else self.body

    def get_read_at_for(self, user):
        if self.sender == user:
            return self.sender_read_at
        if self.recipient == user:
            return self.recipient_read_at

        return None
