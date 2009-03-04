from django.contrib import admin
from acapella.models import PermissionSlip, PermissionProject, PermissionClient

class PermissionSlipAdmin(admin.ModelAdmin):
    list_display = ('slip', 'user', 'permission')
    ordering = ('-slip',)

class PermissionProjectAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'permission')
    ordering = ('-project',)

class PermissionClientAdmin(admin.ModelAdmin):
    list_display = ('client', 'user', 'permission')
    ordering = ('-client',)

admin.site.register(PermissionSlip, PermissionSlipAdmin)
admin.site.register(PermissionProject, PermissionProjectAdmin)
admin.site.register(PermissionClient, PermissionClientAdmin)