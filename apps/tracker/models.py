from django.db import models, IntegrityError
from django.contrib.auth.models import User
import datetime
from math import floor
from project.models import Project


class Slip(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(User, related_name="slips", blank=True, null=True)
    project = models.ForeignKey(Project, blank = True, null=True)
    #client = models.ForeignKey(Client)
    #type = models.CharField(max_length=32)
    due = models.DateField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    def display_time(self):
        seconds = 0
        for slice in self.timeslice_set.all():
            seconds += slice.duration

        delta = datetime.timedelta(0, seconds)

        duration = {
            'days': delta.days,
            'hours': floor(delta.seconds / 3600),
            'minutes': floor((delta.seconds % 3600) / 60),
            'seconds': delta.seconds % 60
        }

        return '%02i:%02i:%02i:%02i' % (duration['days'],duration['hours'],
                                        duration['minutes'],duration['seconds'])
    def display_days_time(self, date):
        seconds = 0
        for slice in self.timeslice_set.filter(slip = self.id, create_date = date):
            seconds += slice.duration

        delta = datetime.timedelta(0, seconds)

        duration = {
            'hours': floor(delta.seconds / 3600),
            'minutes': floor((delta.seconds % 3600) / 60),
        }

        return '%02i.%02i' % (duration['hours'], duration['minutes'])



    def is_active(self):
        slice = self.timeslice_set.filter(end = None)
        return bool(slice)


    class Meta:
        ordering = ["-created"]



class TimeSlice(models.Model):
    begin = models.DateTimeField(default=datetime.datetime.now)
    end = models.DateTimeField(null=True, blank=True)
    slip = models.ForeignKey(Slip)
    user = models.ForeignKey(User, related_name="timeslices", blank=True, null=True)
    duration = models.PositiveIntegerField(editable=False, default=0)
    week_number = models.PositiveIntegerField(default=datetime.datetime.now().isocalendar()[1])
    create_date = models.DateField(default=datetime.datetime.now().date())

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

    def update_date(self):
        self.save()
        pk = self.pk
        self = TimeSlice.objects.get(pk=pk)
        self.week_number = self.begin.isocalendar()[1]
        self.create_date = self.begin.date()
        self.save()

    class Meta:
        ordering = ["-begin"]
