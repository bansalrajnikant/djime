from django.contrib import admin
from djime.models import Slip, TimeSlice, DataImport


class InlineTimeSlice(admin.TabularInline):
    model = TimeSlice
    extra = 2

class SlipAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'display_time']
    inlines = [InlineTimeSlice]

class TimeSliceAdmin(admin.ModelAdmin):
    list_display = ['begin', 'end', 'duration']

class DataImportAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'completed')
    list_filter = ('user', 'completed')
    date_hierarchy = 'created'
    ordering = ('-created',)


admin.site.register(TimeSlice, TimeSliceAdmin)
admin.site.register(Slip, SlipAdmin)
admin.site.register(DataImport, DataImportAdmin)

