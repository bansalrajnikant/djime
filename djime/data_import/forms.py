from django import forms
import mimetypes
import csv
from django.utils.translation import ugettext_lazy as _


FILETYPE_CHOICES = (
    ('timetracker_csv', 'TimeTracker.app CSV file'),
)

class DataImportForm(forms.Form):
    filetype = forms.ChoiceField(choices=FILETYPE_CHOICES)
    import_file = forms.FileField()

    def clean(self):
        cleaned_data = self.cleaned_data
        file = cleaned_data.get("import_file")
        if mimetypes.guess_type(file.name)[0] != 'text/csv':
            raise  forms.ValidationError(_('Invalid file format'))
        dict = csv.DictReader(file, fieldnames=['date','start','end','duration','project','task'])
        list = []
        try:
            for value in dict:
                list.append(value)
        except csv.Error:
            raise  forms.ValidationError(_('You having uploaded a bad file or is very sneaky and have been caught.'))
        return cleaned_data

