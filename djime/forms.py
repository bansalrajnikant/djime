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
        if self.cleaned_data.has_key('project') and self.cleaned_data['project']:
            project = Project.objects.filter(name__iexact=self.cleaned_data['project'], members=self.data['user'])[:1]
            if project:
                return project[0]
            else:
                raise forms.ValidationError(_('%s is not a valid project.' % self.cleaned_data['project']))
        else:
            # If project field was empty, return None as cleaned data.
            return None

    class Meta:
        model = Slip
        fields = ('name', 'client', 'project')


class SlipChangeForm(forms.ModelForm):
    project = forms.CharField(required=False)

    def clean_project(self):
        """
        Cleaning/validation method for the project field
        """
        if self.cleaned_data.has_key('project') and self.cleaned_data['project']:
            project = Project.objects.filter(name__iexact=self.cleaned_data).filter(members=self.data['user'])[:1]
            if project:
                return project[0]
            else:
                raise forms.ValidationError(_('%s is not a valid project.' % self.cleaned_data['project']))
        else:
            return None

    class Meta:
        model = Slip
        fields = ('client', 'project')
