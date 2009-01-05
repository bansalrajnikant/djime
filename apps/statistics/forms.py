from django import forms
import datetime
import re
from exceptions import ValueError

class DateSelectionForm (forms.Form):
    date = forms.CharField()

    def clean(self):
        cleaned_data = self.cleaned_data
        date_data = cleaned_data.get("date")
        if date_data:
            date_list = date_data.split()
            if len(date_list) != 3:
                raise forms.ValidationError("You have to enter 2 dates, in the date field, seperated by SPACE. Hint, use the date picker provided")
            else:
                start_date = date_list[0]
                end_date = date_list[-1]
                if not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", start_date):
                    raise forms.ValidationError("Start date has invalid format, must be 'yyyy-mm-dd'")

                if not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", end_date):
                    raise forms.ValidationError("Start date has invalid format, must be 'yyyy-mm-dd'")

                if not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", start_date) or not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", end_date):
                    if start_date == end_date:
                        raise forms.ValidationError("You have to choose 2 different days")

                start = start_date.split('-')
                end = end_date.split('-')
                try:
                    s_date = datetime.date(int(start[0]),int(start[1]),int(start[2]))
                    a= 0
                except ValueError:
                    a=1
                    raise forms.ValidationError("Start date does not exist")
                try:
                    e_date = datetime.date(int(end[0]),int(end[1]),int(end[2]))
                    b = 0
                except ValueError:
                    raise forms.ValidationError("End date does not exist")
                    b=1

                if a == 0 and b == 0:
                    if e_date.__sub__(s_date) > datetime.timedelta(days=60):
                        raise forms.ValidationError("Difference between end and start date must be lower than 60 days")
                    if e_date.__sub__(s_date) < datetime.timedelta(days=1):
                        raise forms.ValidationError("End date must be after start date")

                    cleaned_data['start'] = start_date
                    cleaned_data['end'] = end_date
        return cleaned_data

class DateSelectionBetaForm (forms.Form):
    team_statistics_date_selection = forms.CharField()

    def clean(self):
        cleaned_data = self.cleaned_data
        date_data = cleaned_data.get("team_statistics_date_selection")
        if date_data:
            date_list = date_data.split()
            if len(date_list) != 3:
                raise forms.ValidationError("You have to enter 2 dates, in the date field, seperated by SPACE. Hint, use the date picker provided")
            else:
                start_date = date_list[0]
                end_date = date_list[-1]
                if not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", start_date):
                    raise forms.ValidationError("Start date has invalid format, must be 'yyyy-mm-dd'")

                if not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", end_date):
                    raise forms.ValidationError("Start date has invalid format, must be 'yyyy-mm-dd'")

                if not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", start_date) or not re.match("[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}$", end_date):
                    if start_date == end_date:
                        raise forms.ValidationError("You have to choose 2 different days")

                start = start_date.split('-')
                end = end_date.split('-')
                try:
                    s_date = datetime.date(int(start[0]),int(start[1]),int(start[2]))
                    a= 0
                except ValueError:
                    a=1
                    raise forms.ValidationError("Start date does not exist")
                try:
                    e_date = datetime.date(int(end[0]),int(end[1]),int(end[2]))
                    b = 0
                except ValueError:
                    raise forms.ValidationError("End date does not exist")
                    b=1

                if a == 0 and b == 0:
                    if e_date.__sub__(s_date) > datetime.timedelta(days=60):
                        raise forms.ValidationError("Difference between end and start date must be lower than 60 days")
                    if e_date.__sub__(s_date) < datetime.timedelta(days=1):
                        raise forms.ValidationError("End date must be after start date")

                    cleaned_data['start'] = start_date
                    cleaned_data['end'] = end_date
        return cleaned_data
