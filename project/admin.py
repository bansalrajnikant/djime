from django.contrib import admin
from project.models import Client, Project


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name']

class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'client', 'deadline']


admin.site.register(Client, ClientAdmin)
admin.site.register(Project, ProjectAdmin)
