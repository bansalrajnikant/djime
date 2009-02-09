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
        # As this method is for the project field, we only get the clean_data for the project.
        cleaned_data = self.cleaned_data['project']
        if cleaned_data:
            # if user choses no project after choosing a client: set cleaned data to None
            if cleaned_data == u'-----------':
                cleaned_data = None
            else:
                project = Project.objects.filter(name__iexact=cleaned_data).filter(members=self.data['user'])
                if project:
                    cleaned_data['project'] = project[0]
                else:
                    raise forms.ValidationError(_('%s is not a valid project.' % cleaned_data))
        # if cleaned_data is an empty string, user has not entered a project: set cleaned data to None
        else:
            cleaned_data = None
        return cleaned_data

    class Meta:
        model = Slip
        fields = ('name', 'client', 'project')

