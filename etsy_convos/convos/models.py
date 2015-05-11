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

    def get_participants(self):
        message = self.get_last_message()
        return User.objects.filter(pk__in=[message.sender.pk, message.recipient.pk])

class ConvoMessage(models.Model):
    """
    Model that houses the main body of the message
    """
    thread = models.ForeignKey(ConvoThread, related_name='convomessages')
    body = models.TextField()
    sender = models.ForeignKey(User, related_name='convomessages_sent')
    sender_read = models.BooleanField(_("Sender read"), default=False)
    sender_deleted_at = models.DateTimeField(_("Sender deleted at"), blank=True, null=True)
    recipient = models.ForeignKey(User, related_name='convomessages_received')
    recipient_read = models.BooleanField(_("Recipient read"), default=False)
    recipient_deleted_at = models.DateTimeField(_("Recipient deleted at"), blank=True, null=True)

    created_at = CreationDateTimeField(_("Created at"), blank=True)

    @property
    def body_excerpt(self):
        return self.body[:49]+'...' if len(self.body) > 50 else self.body

    def get_is_read_for(self, user):
        if self.sender == user:
            return self.sender_read
        if self.recipient == user:
            return self.recipient_read

        return None

    def set_is_read_for(self, user, is_read):
        if self.sender.pk == user.pk:
            self.sender_read = is_read
        if self.recipient.pk == user.pk:
            self.recipient_read = is_read
