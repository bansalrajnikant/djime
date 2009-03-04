from django.contrib import admin
from acapella.models import PermissionSlip, PermissionProject, PermissionClient

class PermissionSlipAdmin(admin.ModelAdmin):
    list_display = ('model', 'user', 'permission')
    ordering = ('-model',)

class PermissionProjectAdmin(admin.ModelAdmin):
    list_display = ('model', 'user', 'permission')
    ordering = ('-model',)

class PermissionClientAdmin(admin.ModelAdmin):
    list_display = ('model', 'user', 'permission')
    ordering = ('-model',)

admin.site.register(PermissionSlip, PermissionSlipAdmin)
admin.site.register(PermissionProject, PermissionProjectAdmin)
admin.site.register(PermissionClient, PermissionClientAdmin)