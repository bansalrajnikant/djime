from django.db import models
from django.contrib.auth.models import User

class Import(models.Model):
    user = models.ForeignKey(User)
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(blank=True, null=True)
    complete_data = models.FileField(upload_to='import_data/complete/%Y/%m/')
    partial_data = models.FileField(upload_to='import_data/partial/%Y/%m/')
