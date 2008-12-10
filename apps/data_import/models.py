from django.db import models
from django.contrib.auth.models import User

class Import(models.Model):
    complete_data = models.FileField(upload_to='import_data/complete/%Y/%m/')
    partial_data = models.FileField(upload_to='import_data/partial/%Y/%m/')
    user = models.ForeignKey(User, blank=False, null=False)
