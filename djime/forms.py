from django import forms
from django.db import models
from django.utils.translation import ugettext as _
from djime.models import Slip
from project.models import Project


class SlipAddForm(forms.ModelForm):
    project = forms.CharField(required=False)

    def clean_project(self):
        """
        Cleaning/validation method for the project field
        """
        cleaned_data = self.cleaned_data
        if cleaned_data.has_key('project'):
            project = Project.objects.filter(name__iexact=cleaned_data['project']).filter(members=self.data['user'])[:1]
            if project:
                return project[0]
            else:
                raise forms.ValidationError(_('%s is not a valid project.' % cleaned_data['project']))

    class Meta:
        model = Slip
        fields = ('name', 'client', 'project')

