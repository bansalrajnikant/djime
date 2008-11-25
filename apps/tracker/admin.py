from django.contrib import admin
from tracker.models import Slip, TimeSlice


class InlineTimeSlice(admin.TabularInline):
    model = TimeSlice
    extra = 2

class SlipAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'display_time']
    inlines = [InlineTimeSlice]

class TimeSliceAdmin(admin.ModelAdmin):
    list_display = ['begin', 'end', 'duration']


admin.site.register(TimeSlice, TimeSliceAdmin)
admin.site.register(Slip, SlipAdmin)
