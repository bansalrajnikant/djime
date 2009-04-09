from django import forms
from django.db import models
from django.utils.translation import ugettext as _
from project.models import Project, Client

class ProjectUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ('state', 'client', 'team', 'name')


class ProjectAddForm(forms.ModelForm):

    class Meta:
        model = Project
        fields = ('name', 'client', 'team')


class ClientAddForm(forms.ModelForm):

    class Meta:
        model = Client
        fields = ('name',)
