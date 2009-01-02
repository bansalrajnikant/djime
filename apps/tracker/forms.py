from django import forms
from tracker.models import Slip

class SlipAddForm(forms.ModelForm):
    class Meta:
        model = Slip
        fields = ('name',)

