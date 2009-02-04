from django import forms
from djime.models import Slip
from django.db import models
from project.models import Project
from django.utils.translation import ugettext as trans


class SlipAddForm(forms.ModelForm):
    project = forms.ModelChoiceField(Project.objects.all(), required=False, widget=forms.widgets.TextInput)
    
    def __init__(self, user, *args, **kwargs):
            super(SlipAddForm, self).__init__(*args, **kwargs)
            self.fields['project'].queryset = Project.objects.filter(members=user)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        data = self.data
        error = self._errors
        if data['input']:
            project = Project.objects.filter(name__iexact=data['input'])
            if not project:
                error['project'] = [trans(u'Project does not exist')]
                data['project'] = data['input']
            else:
                cleaned_data['project'] = project[0].name
                data['project'] = project[0].name
        return cleaned_data
    
    class Meta:
        model = Slip
        fields = ('name', 'client', 'project')
