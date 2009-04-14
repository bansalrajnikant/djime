from django.db import models
from django.contrib.auth.models import User
from teams.models import Team
from django.utils.translation import ugettext_lazy as _

class Client(models.Model):
    """
    A common use case is to do work for different clients.

    Clients could be external customers, other departmens of your company, etc.
    Since we're not creating a CRM here, we'll just keep this model simple.
    """
    name = models.CharField(max_length=128, verbose_name=_('name'))

    def __unicode__(self):
        return self.name

class Project(models.Model):
    """
    A project of some kind

    Acts as a basic container for Slips (tasks)
    """
    STATE_CHOICES = (
        ('active', _('Active')),
        ('on_hold', _('On Hold')),
        ('completed', _('Completed')),
        ('dropped', _('Dropped')),
    )
    name = models.CharField(max_length=128, verbose_name=_('name'))
    description = models.TextField(blank=True)
    team = models.ForeignKey(Team, null=True, blank = True, verbose_name=_('team'))
    client = models.ForeignKey(Client, null=True, blank=True, verbose_name=_('client'))
    members = models.ManyToManyField(User, verbose_name=_('members'))
    deadline = models.DateField(null=True, blank=True, verbose_name=_('deadline'))
    state = models.CharField(max_length=31, choices=STATE_CHOICES, default='active', verbose_name=_('state'))

    def __unicode__(self):
        return self.name
