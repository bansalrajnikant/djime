from django import forms
import datetime
import re
from exceptions import ValueError
from django.utils.translation import ugettext as _

class DateSelectionForm(forms.Form):
    date = forms.CharField()

    def clean(self):
        cleaned_data = self.cleaned_data
        date_data = cleaned_data.get("date")
        # first check that the user has entered 2 values seperated by space
        # something space.
        date_list = date_data.split()
        if len(date_list) != 3:
            raise forms.ValidationError(_("You have to enter 2 dates, in the date field, seperated by SPACE and a DASH (-) and a SPACE. Hint, use the date picker provided"))
        # start and end dates are set from the date list.
        start_date = date_list[0]
        end_date = date_list[-1]
        # use regular expression to check if the user has entered the date in
        # the format 'yyyy-mm-dd'
        if not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", start_date):
            raise forms.ValidationError(_("Start date has invalid format, must be 'yyyy-mm-dd'"))

        if not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", end_date):
            raise forms.ValidationError(_("Start date has invalid format, must be 'yyyy-mm-dd'"))

        # since re test passed, the dates can now be splitted by the
        # dash to create a list with the year, month and day.
        start = start_date.split('-')
        end = end_date.split('-')

        # using try and catching ValueError to check if the user has
        # entered an invalid date like Feb 31 or Jan 55 ect.
        try:
            s_date = datetime.date(int(start[0]),int(start[1]),int(start[2]))
        except ValueError:
            raise forms.ValidationError(_("Start date does not exist"))
        try:
            e_date = datetime.date(int(end[0]),int(end[1]),int(end[2]))
        except ValueError:
            raise forms.ValidationError(_("End date does not exist"))

        # Lastly we check to see that the two dates are between 1 and
        # 60 days apart, and that the begin date is before the end date
        if e_date - (s_date) > datetime.timedelta(days=60):
            raise forms.ValidationError(_("Difference between end and start date must be lower than 60 days"))
        if e_date - (s_date) < datetime.timedelta(days=1):
            raise forms.ValidationError(_("End date must be after start date"))

        cleaned_data['start'] = s_date
        cleaned_data['end'] = e_date
        # Always returning the cleaned data.
        return cleaned_data