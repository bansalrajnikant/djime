from django import forms
from djime.models import Slip
from django.db import models
from project.models import Project
from django.utils.translation import ugettext as _


class SlipAddForm(forms.ModelForm):
    project = forms.ModelChoiceField(Project.objects.all(), required=False, widget=forms.widgets.TextInput)
    
    def __init__(self, user, *args, **kwargs):
            super(SlipAddForm, self).__init__(*args, **kwargs)
            self.fields['project'].queryset = Project.objects.filter(members=user)
    
    def clean(self):
        cleaned_data = self.cleaned_data
        data = self.data
        error = self._errors
        # not_a_member: a value to track if the user is member of project(s) found
        not_a_member = True 
        # Check to see if input contains something => 
        # project field is filled in the form
        if data.has_key('input'):
            # get projects by a non case sensetive seach on the project name
            projects = Project.objects.filter(name__iexact=data['input'])
            # if no project could be found send error message and set
            # not a member to False.
            if not projects:
                error['project'] = [_(u'Project does not exist')]
                data['project'] = data['input']
                not_a_member = False
            else:
                # If we do get something back on our search, it will be in a
                # list. There can be more than one result. Iterate to see if
                # the user is member of any of the projects. We are satisfied
                # if we find one project that the user is member of. We wont
                # Support if the user is member of more than one project of the
                # same name, and try to figure out which project the alip should
                # join. In this case the slip will be placed under the last
                # project that matches.
                for project in projects:
                    if data['user'] in project.members.all():
                        cleaned_data['project'] = project.name
                        data['project'] = project.name
                        not_a_member = False

                # if projects was found but the user was not a member in any of them
                # not a member will be true and error message is sent.
                if not_a_member:
                    error['project'] = [_('You are not a member of this project.')]
                    data['project'] = project.name
                
        return cleaned_data
    
    class Meta:
        model = Slip
        fields = ('name', 'client', 'project')
