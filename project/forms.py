from django import forms
from django.db import models
from django.utils.translation import ugettext as _
from project.models import Project

class ProjectUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Project
        fields = ('state', 'client')