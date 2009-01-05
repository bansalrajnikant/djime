from django.contrib import admin
from data_import.models import Import

class ImportAdmin(admin.ModelAdmin):
    list_display = ('user', 'created', 'completed')
    list_filter = ('user', 'completed')
    date_hierarchy = 'created'
    ordering = ('-created',)

admin.site.register(Import, ImportAdmin)
