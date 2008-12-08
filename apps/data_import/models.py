from django.db import models
from django.contrib.auth.models import User

class Import(models.Model):
    complete_data = models.TextField()
    partial_data = models.TextField()
    user = models.ForeignKey(User, blank=False, null=False)
