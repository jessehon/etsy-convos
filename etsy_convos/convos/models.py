# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

class ConvoThreadQuerySet(models.query.QuerySet):
    def active_for(self, user):
        """
        Returns all threads that have at least one active (not deleted) message
        """
        messages = ConvoMessage.objects.active_for(user)
        return self.filter(convomessages__in=messages).distinct().order_by('id')

    def inbox_for(self, user):
        """
        Returns all threads that have at least one active (not deleted) message and
        contains at least a message that was received by the given user
        """
        messages = ConvoMessage.objects.active_for(user).received_by(user)
        return self.filter(convomessages__in=messages).distinct().order_by('id')

    def outbox_for(self, user):
        """
        Returns all threads that have at least one active (not deleted) message and
        contains at least a message that was sent by the given user
        """
        messages = ConvoMessage.objects.active_for(user).sent_by(user)
        return self.filter(convomessages__in=messages).distinct().order_by('id')

class ConvoThreadManager(models.Manager):
    def get_queryset(self):
        return ConvoThreadQuerySet(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_queryset(), attr, *args)


class ConvoThread(models.Model):
    """
    Model used to group related messages together
    """
    subject = models.CharField(max_length=140)

    objects = ConvoThreadManager()

    def get_last_message_for(self, user):
        return self.get_messages_for(user).last()

    def get_participants(self):
        message = self.convomessages.first()
        return User.objects.filter(pk__in=[message.sender.pk, message.recipient.pk])

    def get_messages_for(self, user):
        return self.convomessages.active_for(user)

class ConvoMessageQuerySet(models.query.QuerySet):
    def active_for(self, user):
        active_sent_by = Q(sender=user) & Q(sender_deleted_at__isnull=True)
        active_received_by = Q(recipient=user) & Q(recipient_deleted_at__isnull=True)
        return self.filter(active_sent_by | active_received_by)

    def sent_by(self, user):
        return self.filter(sender=user)

    def received_by(self, user):
        return self.filter(recipient=user)

class ConvoMessageManager(models.Manager):
    def get_queryset(self):
        return ConvoMessageQuerySet(self.model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_queryset(), attr, *args)

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

    objects = ConvoMessageManager()

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
