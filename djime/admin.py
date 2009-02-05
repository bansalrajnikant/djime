from django.contrib import admin
from djime.models import Slip, TimeSlice, DataImport


class InlineTimeSlice(admin.TabularInline):
    model = TimeSlice
    extra = 2

class SlipAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    inlines = (InlineTimeSlice,)
    list_display = ('name', 'user', 'created', 'display_time', 'project', 'client')
    list_filter = ('user', 'project', 'client')
    ordering = ('-created',)
    search_fields = ('name',)

class TimeSliceAdmin(admin.ModelAdmin):
    date_hierarchy = 'begin'
    list_display = ('begin', 'end', 'duration', 'slip', 'user')
    list_filter = ('user', 'begin')
    ordering = ('-begin',)

class DataImportAdmin(admin.ModelAdmin):
    date_hierarchy = 'created'
    list_display = ('user', 'created', 'completed')
    list_filter = ('user', 'completed')
    ordering = ('-created',)


admin.site.register(TimeSlice, TimeSliceAdmin)
admin.site.register(Slip, SlipAdmin)
admin.site.register(DataImport, DataImportAdmin)

