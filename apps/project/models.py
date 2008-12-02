from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    """
    A common use case is to do work for different clients.

    Clients could be external customers, other departmens of your company, etc.
    Since we're not creating a CRM here, we'll just keep this model simple.
    """
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name

class Project(models.Model):
    """
    A project of some kind

    Acts as a basic container for Slips (tasks)
    """
    name = models.CharField(max_length=128)
    client = models.ForeignKey(Client, null=True, blank=True)
    members = models.ManyToManyField(User)
    deadline = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return self.name
