from django.db import models

class Slip(models.Model):
    name = models.CharField(max_length=128)
    #project = models.ForeignKey(Project)
    #client = models.ForeignKey(Client)
    #type = models.CharField(max_length=32)
    due = models.DateField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created"]

class TimeSlice(models.Model):
    begin = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    slip = models.ForeignKey(Slip)

    class Meta:
        ordering = ["-begin"]
