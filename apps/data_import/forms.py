from django import forms

FILETYPE_CHOICES = (
    ('timetracker_csv', 'TimeTracker.app CSV file'),
)

class DataImportForm(forms.Form):
    filetype = forms.ChoiceField(choices=FILETYPE_CHOICES)
    import_file = forms.FileField()
