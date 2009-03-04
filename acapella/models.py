from django.db import models
from django.contrib.auth.models import User
from djime.models import Slip
from project.models import Project, Client

class Permission(models.Model):
    """
    This model is the base form, for models that will create a ACL.

    The structure for the permission model is still a bit uncertain, as it is
    still in progress. The idea is to create subclasses of this model, one for
    each model that need a ACL
    """

    PERMISSION_CHOICES = (
        (0, 'No access'),
        (1, 'Read'),
        (2, 'Write'),
        (3, 'Read and write'),
        (4, 'Delete'),
        (5, 'View and delete'),
        (6, 'Write and delete'),
        (7, 'Read, write and delete'),
    )
    permission = models.IntegerField(default=0, choices=PERMISSION_CHOICES)
    user = models.ForeignKey(User)


class PermissionSlip(Permission):
    """
    This is the permission model for slips.
    """

    model = models.ForeignKey(Slip)

    def __unicode__(self):
        return self.model.__unicode__() + ': ' + self.PERMISSION_CHOICES[self.permission][1]

class PermissionProject(Permission):
    """
    This is the permission model for projets.
    """

    model = models.ForeignKey(Project)

    def __unicode__(self):
        return self.model.__unicode__() + ': ' + self.PERMISSION_CHOICES[self.permission][1]

class PermissionClient(Permission):
    """
    This is the permission model for projets.
    """

    model = models.ForeignKey(Client)

    def __unicode__(self):
        return self.model.__unicode__() + ': ' + self.PERMISSION_CHOICES[self.permission][1]