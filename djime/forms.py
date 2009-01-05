from django import forms
from djime.models import Slip

class SlipAddForm(forms.ModelForm):
    class Meta:
        model = Slip
        fields = ('name',)

