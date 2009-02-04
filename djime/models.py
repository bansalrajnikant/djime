import datetime
from math import floor
from django.db import models, IntegrityError
from django.contrib.auth.models import User
from project.models import Project, Client
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import pre_save
from djime.signals import timeslice_save


class Slip(models.Model):
    name = models.CharField(max_length=128, verbose_name=_('name'))
    user = models.ForeignKey(User, related_name="slips", blank=True, null=True, verbose_name=_('user'))
    project = models.ForeignKey(Project, blank = True, null=True, verbose_name=_('project'))
    client = models.ForeignKey(Client, blank = True, null=True, verbose_name=_('client'))
    #type = models.CharField(max_length=32)
    due = models.DateField(null=True, blank=True, verbose_name=_('due'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    updated = models.DateTimeField(auto_now=True, verbose_name=_('updated'))

    def __unicode__(self):
        return self.name

    def display_time(self):
        seconds = 0
        for slice in self.timeslice_set.all():
            seconds += slice.duration

        delta = datetime.timedelta(0, seconds)

        duration = {
            'hours': floor(delta.seconds / 3600) + delta.days * 24,
            'minutes': floor((delta.seconds % 3600) / 60)
        }

        return '%02i:%02i' % (duration['hours'], duration['minutes'])


    def display_days_time(self, date):
        seconds = 0
        for slice in self.timeslice_set.filter(begin__year=date.year, begin__month=date.month, begin__day=date.day):
            seconds += slice.duration
        return seconds

    def is_active(self):
        slice = self.timeslice_set.filter(end = None)
        return bool(slice)

    class Meta:
        ordering = ["-created"]



class TimeSlice(models.Model):
    begin = models.DateTimeField(default=datetime.datetime.now, verbose_name=_('begin'))
    end = models.DateTimeField(null=True, blank=True, verbose_name=_('end'))
    slip = models.ForeignKey(Slip, verbose_name=_('slip'))
    user = models.ForeignKey(User, related_name="timeslices", blank=True, null=True, verbose_name=_('user'))
    duration = models.PositiveIntegerField(editable=False, default=0, verbose_name=_('duration'))
    week_number = models.PositiveIntegerField(default=datetime.datetime.now().isocalendar()[1], verbose_name=_('week number'))

    def __unicode__(self):
        if self.duration == 0:
            self.update_duration()

        if self.duration:
            delta = datetime.timedelta(seconds=self.duration)
            return _('%(days)i days, %(seconds)i seconds') % {'days': delta.days, 'seconds': delta.seconds}
        if self.end:
            return _('From %(begin)s to %(end)s') % {'begin': self.begin, 'end': self.end}
        else:
            return _('From %(begin)s') % {'begin': self.begin}

    class Meta:
        ordering = ["-begin"]

class DataImport(models.Model):
    user = models.ForeignKey(User, verbose_name=_('user'))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_('created'))
    completed = models.DateTimeField(blank=True, null=True, verbose_name=_('completed'))
    complete_data = models.FileField(upload_to='import_data/complete/%Y/%m/', verbose_name=_('complete data'))
    partial_data = models.FileField(upload_to='import_data/partial/%Y/%m/', verbose_name=_('partial data'))
    

pre_save.connect(timeslice_save, sender=TimeSlice)