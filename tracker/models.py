from django.db import models
from django.contrib.auth.models import User
import datetime

class Slip(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, related_name="slips", blank=True, null=True)
    #project = models.ForeignKey(Project)
    #client = models.ForeignKey(Client)
    #type = models.CharField(max_length=32)
    due = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["-created"]

class TimeSlice(models.Model):
    begin = models.DateTimeField(auto_now_add=True)
    end = models.DateTimeField(null=True, blank=True)
    slip = models.ForeignKey(Slip)
    user = models.ForeignKey(User, related_name="timeslices", blank=True, null=True)
    duration = models.PositiveIntegerField(editable=False, default=0)

    def __unicode__(self):
        if self.duration == 0:
            self.update_duration()

        if self.duration:
            delta = datetime.timedelta(seconds=self.duration)
            return '%i days, %i seconds' % (delta.days, delta.seconds)
        if self.end:
            return 'From %s to %s' % (self.begin, self.end)
        else:
            return 'From %s' % self.begin

    def update_duration(self):
        if self.end:
            time = self.end - self.begin
            self.duration = time.days * 86400 + time.seconds
            self.save()
        else:
            self.duration = 0
            self.save()

    class Meta:
        ordering = ["-begin"]
