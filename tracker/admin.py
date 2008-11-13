from django.contrib import admin
from djime.tracker.models import Slip, TimeSlice

class SlipAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'display_time']

class TimeSliceAdmin(admin.ModelAdmin):
    list_display = ['begin', 'end', 'duration']


admin.site.register(TimeSlice, TimeSliceAdmin)
admin.site.register(Slip, SlipAdmin)
