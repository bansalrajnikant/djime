import datetime
import time
from django.contrib.auth.models import User
from djime.models import TimeSlice
from djime.statistics.colour import colour
from exceptions import ImportError
try:
    import json
except ImportError:
    from django.utils import simplejson as json
from django.utils.translation import ugettext as _ #note, we dont use ugettext_lazy as we use json or simplejson to generate json data.

def user_week_json(user, week, year):
    slice_query_set = TimeSlice.objects.filter(week_number=week, begin__year= year, user = user)
    # start date is set to a day in the week before the week we want to search.
    start_date = datetime.date(year, 1, 1) + datetime.timedelta(days = (week-2)*7)
    # this while loop will keep adding a day to the start date, until first day of the week is reached
    # thus start_date with be the first day of the week
    while start_date.isocalendar()[1] != week:
        start_date += datetime.timedelta(days=1)

    end_date = start_date + datetime.timedelta(days=6)
    while_loop_date = start_date
    date_slip_dict = {}
    sorted_date_list = []
    # this while loop generates every day every and adds that day to dictionary and list
    while while_loop_date != end_date + datetime.timedelta(days=1):
        date_slip_dict[while_loop_date]=[]
        sorted_date_list.append(while_loop_date)
        while_loop_date += datetime.timedelta(days=1)
    
    # this loop checks to see if a given slip of a timeslice is added to the list of that day.
    # if it hasn't been added yet it adds it to the list of slips containing timeslices made that day.
    for slice in slice_query_set:
        if slice.slip not in date_slip_dict[slice.begin.date()]:
            date_slip_dict[slice.begin.date()].append(slice.slip)
    
    # the value_dictionary, will be the dictionary that needs to be converted to json data. A lot of the data is static strings,
    # but there are 6 varibles that are different. 2 empty lists where data will be appended (values and labels list) and 4 values set to True.
    # can add a colour generator later to create colours for the graph instead of static colours.
    value_dictionary = {}
    value_dictionary['elements'] = [{"tip": _("#key#<br>Time: #gmdate:H.i# Total: #totalgmdate:H.i#"), "type": "bar_stack", "colours": ["#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF"], "values": []}]
    value_dictionary['title'] = {"text": True, "style": "{font-size: 20px; color: #000000; text-align: center;}"}
    value_dictionary['x_axis'] = {"labels": { "labels": []}}
    value_dictionary['y_axis'] = { "min": 0, "max": True, "labels": {"text":"#gmdate:H:i#", "labels": []}}
    value_dictionary['tooltip'] = {"mouse": 2}

    max_list = [0.01]
    # this loop has 2 purposes. First is to generate a list with values, each value in the list will be a dictionary - the while_dictionary,
    # which has 2 keys, val, which will hold the actual value a float, and tip, which will hold the data for the tooltip, a string.
    # Second purpose is to find the max value for the date period to scale the y_axis.
    for date in sorted_date_list:
        value_dictionary['x_axis']['labels']['labels'].append(date.strftime('%A'))
        i=0
        temp_max = 0.0
        value_list = []
        if len(date_slip_dict[date]) == 0:
            value_dictionary['elements'][0]['values'].append([0])   # if len = 0, there are no items, so the while loop wont activate, and we can simply add [0]
        else:
            while i < len(date_slip_dict[date]):
                while_dictionary = {'val': True, 'key': True}
                while_dictionary['val'] = date_slip_dict[date][i].display_days_time(date)
                while_dictionary['key'] = '%s' % date_slip_dict[date][i].name
                temp_max += date_slip_dict[date][i].display_days_time(date)
                value_list.append(while_dictionary)
                i += 1
            max_list.append(temp_max)
            value_dictionary['elements'][0]['values'].append(value_list)

    value_dictionary['y_axis']['max']=max(max_list)
    value_dictionary['y_axis']['min']=0
    step = max(max_list) * 0.1
    for numb in range(11):
        y_time = numb*step
        value_dictionary['y_axis']['labels']['labels'].append({'y': y_time})

    value_dictionary['title']['text'] = _('%(username)s Week: %(week)s Year: %(year)s') % {'username': user.username, 'week': week, 'year': year}

    return json.dumps(value_dictionary)


def user_month_json(user, month, year):
    #this function is basicly the same as week, only start date can be found getting day 1 of the chosen month and year.
    # the end day is gotten by either getting it in the long month by adding 30 days or in the short months subtracking days in a while loop
    # until a day in the chosen month is gotten which is the last day of that month.
    # also the labels is a bit different showing day numbers instead of weekday names.
    start_date = datetime.date(year, month, 1)
    end_date = start_date + datetime.timedelta(days=30)
    while end_date.month != start_date.month:
        end_date -= datetime.timedelta(days=1)

    w_date = start_date
    date_slip_dict = {}
    sorted_date_list = []
    while w_date != end_date + datetime.timedelta(days=1):
        date_slip_dict[w_date]=[]
        sorted_date_list.append(w_date)
        w_date += datetime.timedelta(days=1)

    slice_query_set = TimeSlice.objects.filter(user = user, begin__range=(start_date, end_date))
    for slice in slice_query_set:
        if slice.slip not in date_slip_dict[slice.begin.date()]:
            date_slip_dict[slice.begin.date()].append(slice.slip)

    value_dictionary = {}
    value_dictionary['elements'] = [{"tip": _("#key#<br>Time: #gmdate:H.i# Total: #totalgmdate:H.i#"), "type": "bar_stack", "colours": ["#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF"], "values": []}]
    value_dictionary['title'] = {"text": True, "style": "{font-size: 20px; color: #000000; text-align: center;}"}
    value_dictionary['x_axis'] = {"labels": {"labels": []}}
    value_dictionary['y_axis'] = { "min": 0, "max": True, "labels": {"text":"#gmdate:H:i#", "labels": []}}
    value_dictionary['tooltip'] = {"mouse": 2}

    max_list = [0.01]
    for date in sorted_date_list:
        value_dictionary['x_axis']['labels']['labels'].append(str(date.day))
        i=0
        temp_max = 0.0
        value_list = []
        if len(date_slip_dict[date]) == 0:
            value_dictionary['elements'][0]['values'].append([0])
        else:
            while i < len(date_slip_dict[date]):
                while_dictionary = {'val': True, 'key': True}
                while_dictionary['val'] = date_slip_dict[date][i].display_days_time(date)
                while_dictionary['key'] = '%s' % date_slip_dict[date][i].name
                temp_max += date_slip_dict[date][i].display_days_time(date)
                value_list.append(while_dictionary)
                i += 1
            max_list.append(temp_max)
            value_dictionary['elements'][0]['values'].append(value_list)

    value_dictionary['y_axis']['max'] = max(max_list)
    value_dictionary['y_axis']['min'] = 0
    step = max(max_list) * 0.1
    for numb in range(11):
        value_dictionary['y_axis']['labels']['labels'].append({'y': numb*step})

    value_dictionary['title']['text'] = _('%(username)s %(month)s %(year)s') % {'username': user.username, 'month': start_date.strftime('%B'), 'year': year}
    return json.dumps(value_dictionary)


def user_date_json(user, start_date, end_date):
    # the method is again the same.
    # we want start and end date to have the format: u'yyyy-mm-dd'
    s_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    w_date = s_date
    date_slip_dict = {}
    sorted_date_list = []
    while w_date != e_date + datetime.timedelta(days=1):
        date_slip_dict[w_date]=[]
        sorted_date_list.append(w_date)
        w_date += datetime.timedelta(days=1)

    slice_query_set = TimeSlice.objects.filter(user = user, begin__range=(s_date, e_date))
    for slice in slice_query_set:
        if slice.slip not in date_slip_dict[slice.begin.date()]:
            date_slip_dict[slice.begin.date()].append(slice.slip)

    value_dictionary = {}
    value_dictionary['elements'] = [{"tip": _("#key#<br>Time: #gmdate:H.i# Total: #totalgmdate:H.i#"), "type": "bar_stack", "colours": ["#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF"], "values": []}]
    value_dictionary['title'] = {"text": True, "style": "{font-size: 20px; color: #000000; text-align: center;}"}
    value_dictionary['x_axis'] = {"labels": { "labels": []}}
    value_dictionary['y_axis'] = { "min": 0, "max": True, "labels": {"text":"#gmdate:H:i#", "labels": []}}
    value_dictionary['tooltip'] = {"mouse": 2}

    max_list = [0.01]
    for date in sorted_date_list:
        value_dictionary['x_axis']['labels']['labels'].append(str(date.day))
        i=0
        temp_max = 0.0
        value_list = []
        if len(date_slip_dict[date]) == 0:
            value_dictionary['elements'][0]['values'].append([0])
        else:
            while i < len(date_slip_dict[date]):
                while_dictionary = {'val': True, 'key': True}
                while_dictionary['val'] = date_slip_dict[date][i].display_days_time(date)
                while_dictionary['key'] = '%s' % date_slip_dict[date][i].name
                temp_max += date_slip_dict[date][i].display_days_time(date)
                value_list.append(while_dictionary)
                i += 1
            max_list.append(temp_max)
            value_dictionary['elements'][0]['values'].append(value_list)

    value_dictionary['y_axis']['max'] = max(max_list)
    step = max(max_list) * 0.1
    for numb in range(11):
        value_dictionary['y_axis']['labels']['labels'].append({'y': numb*step})

        value_dictionary['title']['text'] = _('%(username)s %(start_date)s to %(end_date)s') % {'username': user.username, 'start_date': start_date, 'end_date': end_date}

    return json.dumps(value_dictionary)


def team_week_json(team, week, year):
    # first get a list with user ids for the team, and then use the "user__in = list" filter method
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    slice_query_set = TimeSlice.objects.filter(week_number=week, begin__year= year, user__in = members_id)

    start_date = datetime.date(year, 1, 1) + datetime.timedelta(days = (week-2)*7)
    while start_date.isocalendar()[1] != week:
        start_date += datetime.timedelta(days=1)

    end_date = start_date + datetime.timedelta(days=6)
    w_date = start_date
    date_slip_dict = {}
    sorted_date_list = []
    while w_date != end_date + datetime.timedelta(days=1):
        date_slip_dict[w_date]=[]
        sorted_date_list.append(w_date)
        w_date += datetime.timedelta(days=1)

    for slice in slice_query_set:
        if slice.slip not in date_slip_dict[slice.begin.date()]:
            date_slip_dict[slice.begin.date()].append(slice.slip)

    value_dictionary = {}
    value_dictionary['elements'] = [{"tip": _("#key#<br>Time: #gmdate:H.i# Total: #totalgmdate:H.i#"), "type": "bar_stack", "colours": ["#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF"], "values": []}]
    value_dictionary['title'] = {"text": True, "style": "{font-size: 20px; color: #000000; text-align: center;}"}
    value_dictionary['x_axis'] = {"labels": { "labels": []}}
    value_dictionary['y_axis'] = { "min": 0, "max": True, "labels": {"text":"#gmdate:H:i#", "labels": []}}
    value_dictionary['tooltip'] = {"mouse": 2}

    max_list = [0.01]
    for date in sorted_date_list:
        value_dictionary['x_axis']['labels']['labels'].append(date.strftime('%A'))
        i=0
        temp_max = 0.0
        value_list = []
        if len(date_slip_dict[date]) == 0:
            value_dictionary['elements'][0]['values'].append([0])   # if len = 0, there are no items, so the while loop wont activate, and we can simply add [0]
        else:
            while i < len(date_slip_dict[date]):
                while_dictionary = {'val': True, 'key': True}
                while_dictionary['val'] = date_slip_dict[date][i].display_days_time(date)
                while_dictionary['key'] = '%s' % date_slip_dict[date][i].name
                temp_max += date_slip_dict[date][i].display_days_time(date)
                value_list.append(while_dictionary)
                i += 1
            max_list.append(temp_max)
            value_dictionary['elements'][0]['values'].append(value_list)

    value_dictionary['y_axis']['max']=max(max_list)
    value_dictionary['y_axis']['min']=0
    step = max(max_list) * 0.1
    for numb in range(11):
        y_time = numb*step
        value_dictionary['y_axis']['labels']['labels'].append({'y': y_time})

    value_dictionary['title']['text'] = _('%(team)s Week: %(week)s Year: %(year)s') % {'team': team.name, 'week': week, 'year': year}

    return json.dumps(value_dictionary)


def team_month_json(team, month, year):
    start_date = datetime.date(year, month, 1)
    end_date = start_date + datetime.timedelta(days=30)
    while end_date.month != start_date.month:
        end_date -= datetime.timedelta(days=1)

    w_date = start_date
    date_slip_dict = {}
    sorted_date_list = []
    while w_date != end_date + datetime.timedelta(days=1):
        date_slip_dict[w_date]=[]
        sorted_date_list.append(w_date)
        w_date += datetime.timedelta(days=1)

    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    slice_set = TimeSlice.objects.filter(user__in = members_id, begin__range=(start_date, end_date))

    for slice in slice_set:
        if slice.slip not in date_slip_dict[slice.begin.date()]:
            date_slip_dict[slice.begin.date()].append(slice.slip)

    value_dictionary = {}
    value_dictionary['elements'] = [{"tip": _("#key#<br>Time: #gmdate:H.i# Total: #totalgmdate:H.i#"), "type": "bar_stack", "colours": ["#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF"], "values": []}]
    value_dictionary['title'] = {"text": True, "style": "{font-size: 20px; color: #000000; text-align: center;}"}
    value_dictionary['x_axis'] = {"labels": {"labels": []}}
    value_dictionary['y_axis'] = { "min": 0, "max": True, "labels": {"text":"#gmdate:H:i#", "labels": []}}
    value_dictionary['tooltip'] = {"mouse": 2}

    max_list = [0.01]
    for date in sorted_date_list:
        value_dictionary['x_axis']['labels']['labels'].append(str(date.day))
        i=0
        temp_max = 0.0
        value_list = []
        if len(date_slip_dict[date]) == 0:
            value_dictionary['elements'][0]['values'].append([0])
        else:
            while i < len(date_slip_dict[date]):
                while_dictionary = {'val': True, 'key': True}
                while_dictionary['val'] = date_slip_dict[date][i].display_days_time(date)
                while_dictionary['key'] = '%s' % date_slip_dict[date][i].name
                temp_max += date_slip_dict[date][i].display_days_time(date)
                value_list.append(while_dictionary)
                i += 1
            max_list.append(temp_max)
            value_dictionary['elements'][0]['values'].append(value_list)

    value_dictionary['y_axis']['max'] = max(max_list)
    value_dictionary['y_axis']['min'] = 0
    step = max(max_list) * 0.1
    for numb in range(11):
        value_dictionary['y_axis']['labels']['labels'].append({'y': numb*step})

    value_dictionary['title']['text'] = _('%(team)s %(month)s %(year)s') % {'team': team.name, 'month': start_date.strftime('%B'), 'year': year}

    return json.dumps(value_dictionary)


def team_date_json(team, start_date, end_date):
    # the method is the same as user.
    # we want start and end date to have the format: u'yyyy-mm-dd'
    s_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

    w_date = s_date
    date_slip_dict = {}
    sorted_date_list = []
    while w_date != e_date + datetime.timedelta(days=1):
        date_slip_dict[w_date]=[]
        sorted_date_list.append(w_date)
        w_date += datetime.timedelta(days=1)

    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    slice_set = TimeSlice.objects.filter(user__in = members_id, begin__range=(s_date, e_date))

    for slice in slice_set:
        if slice.slip not in date_slip_dict[slice.begin.date()]:
            date_slip_dict[slice.begin.date()].append(slice.slip)

    value_dictionary = {}
    value_dictionary['elements'] = [{"tip": _("#key#<br>Time: #gmdate:H.i# Total: #totalgmdate:H.i#"), "type": "bar_stack", "colours": ["#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF"], "values": []}]
    value_dictionary['title'] = {"text": True, "style": "{font-size: 20px; color: #000000; text-align: center;}"}
    value_dictionary['x_axis'] = {"labels": { "labels": []}}
    value_dictionary['y_axis'] = { "min": 0, "max": True, "labels": {"text":"#gmdate:H:i#", "labels": []}}
    value_dictionary['tooltip'] = {"mouse": 2}

    max_list = [0.01]
    for date in sorted_date_list:
        value_dictionary['x_axis']['labels']['labels'].append(str(date.day))
        i=0
        temp_max = 0.0
        value_list = []
        if len(date_slip_dict[date]) == 0:
            value_dictionary['elements'][0]['values'].append([0])
        else:
            while i < len(date_slip_dict[date]):
                while_dictionary = {'val': True, 'key': True}
                while_dictionary['val'] = date_slip_dict[date][i].display_days_time(date)
                while_dictionary['key'] = '%s' % date_slip_dict[date][i].name
                temp_max += date_slip_dict[date][i].display_days_time(date)
                value_list.append(while_dictionary)
                i += 1
            max_list.append(temp_max)
            value_dictionary['elements'][0]['values'].append(value_list)

    value_dictionary['y_axis']['max'] = max(max_list)
    step = max(max_list) * 0.1
    for numb in range(11):
        value_dictionary['y_axis']['labels']['labels'].append({'y': numb*step})

    value_dictionary['title']['text'] = _('%(team)s %(start)s to %(end)s') % ('team': team.name, 'start': start_date, 'end': end_date)

    return json.dumps(value_dictionary)


def team_stat_week_json(team, week, year):
    # the method for getting team specific data is gennerally the same as with team/user data.
    # However as the charts work a bit different using bar and scatter_line, the actual data needed to be generated and the setup is a bit different
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)

    slice_set = TimeSlice.objects.filter(week_number=week, begin__year= year, user__in = members_id)
    start_date = datetime.date(year, 1, 1) + datetime.timedelta(days = (week-2)*7)
    while start_date.isocalendar()[1] != week:
        start_date += datetime.timedelta(days=1)
    end_date = start_date + datetime.timedelta(days=6)

    team_list_dict = {}
    counter = 0
    for mem_id in members_id:
        team_list_dict[mem_id] = {}
        team_list_dict[mem_id]['value'] = {"type": "bar", "values": [], "tip": _("%s<br>Time: #gmdate:H.i#") % User.objects.get(pk=mem_id).username, "colour": colour(counter)}
        counter += 1

    sorted_date_list = []
    w_date = start_date
    while w_date != end_date+datetime.timedelta(days=1):
        sorted_date_list.append(w_date)
        for mem_id in members_id:
            team_list_dict[mem_id][w_date]=[]
        w_date += datetime.timedelta(days=1)

    for slice in slice_set:
        if slice.slip not in team_list_dict[slice.user_id][slice.begin.date()]:
            team_list_dict[slice.user_id][slice.begin.date()].append(slice.slip)

    # the value_dictionary has a bit different layout for the team_stat views. elements is now an empty list, where dictionaries can be added.
    # You need 1 dictionary for each set of bars/scatter_line you want to add to your graph. Tooltip and colour can be added imediately,
    # so only a list of numbers/chords are needed.
    value_dictionary = {}
    value_dictionary['elements'] = []
    value_dictionary['title'] = {"text": True, "style": "{font-size: 20px; color: #000000; text-align: center;}"}
    value_dictionary['x_axis'] = {"labels": { "labels": []}}
    value_dictionary['y_axis'] = { "min": 0, "max": True, "labels": {"text":"#gmdate:H:i#", "labels": []}}
    value_dictionary['tooltip'] = {"mouse": 2}

    # this loop works pretty much like the others, however, in this one we need to iterate over the member_ids aswell.
    # in this loop, values can be added one at a time, instead of adding a list of values.
    max_list = [0.01]
    for date in sorted_date_list:
        value_dictionary['x_axis']['labels']['labels'].append(date.strftime('%A'))
        for mem_id in members_id:
            i = 0
            temp_value = 0.0
            while i < len(team_list_dict[mem_id][date]):
                temp_value += team_list_dict[mem_id][date][i].display_days_time(date)
                i += 1
            team_list_dict[mem_id]['value']['values'].append(temp_value)
            max_list.append(temp_value)

    for mem_id in members_id:
        value_dictionary['elements'].append(team_list_dict[mem_id]['value'])

    value_dictionary['y_axis']['max'] = max(max_list)
    step = max(max_list) * 0.1
    for numb in range(11):
        value_dictionary['y_axis']['labels']['labels'].append({'y': numb*step})

    value_dictionary['title']['text'] = _('%(team)s Week: %(week)s Year: %(year)s') % {'team': team.name, 'week': week, 'year': year}

    return json.dumps(value_dictionary)


def team_stat_month_json(team, month, year):
    # uses same method as above.
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)

    month = int(month)
    year = int(year)
    start_date = datetime.date(year, month, 1)
    end_date = start_date + datetime.timedelta(days=30)
    while end_date.month != start_date.month:
        end_date -= datetime.timedelta(days=1)

    slice_set = TimeSlice.objects.filter(begin__range=(start_date, end_date), user__in=members_id)
    team_list_dict = {}
    counter = 0
    for mem_id in members_id:
        team_list_dict[mem_id] = {}
        team_list_dict[mem_id]['value'] = {"type": "scatter_line", "values": [], _("tip": "%(username)s<br>Time: #ygmdate:H:i#") % {'username': User.objects.get(pk=mem_id).username}, "colour": colour(counter)}
        counter += 1

    sorted_date_list = []
    w_date = start_date
    while w_date != end_date + datetime.timedelta(days=1):
        sorted_date_list.append(w_date)
        for mem_id in members_id:
            team_list_dict[mem_id][w_date]=[]
        w_date += datetime.timedelta(days=1)

    for slice in slice_set:
        if slice.slip not in team_list_dict[slice.user_id][slice.begin.date()]:
            team_list_dict[slice.user_id][slice.begin.date()].append(slice.slip)

    value_dictionary = {}
    value_dictionary['elements'] = []
    value_dictionary['title'] = {"text": True, "style": "{font-size: 20px; color: #000000; text-align: center;}"}
    value_dictionary['x_axis'] = {"min": 0, "max": True}
    value_dictionary['y_axis'] = { "min": 0, "max": True, "labels": {"text":"#gmdate:H:i#", "labels": []}}
    value_dictionary['tooltip'] = {"mouse": 1}

    max_list = [0.01]
    for date in sorted_date_list:
        for mem_id in members_id:
            i = 0
            temp_value = 0.0
            temp_value_dict = {'x': True, 'y': True} # in this case chords in the form of a dictionary is added as a value, instead of a float.
            while i < len(team_list_dict[mem_id][date]):
                temp_value += team_list_dict[mem_id][date][i].display_days_time(date)
                i += 1
            temp_value_dict['x'] = date.day
            temp_value_dict['y'] = temp_value
            team_list_dict[mem_id]['value']['values'].append(temp_value_dict)
            max_list.append(temp_value)

    for mem_id in members_id:
        value_dictionary['elements'].append(team_list_dict[mem_id]['value'])

    value_dictionary['y_axis']['max'] = max(max_list) * 1.05
    step = max(max_list) * 1.05 * 0.1
    for numb in range(11):
        value_dictionary['y_axis']['labels']['labels'].append({'y': numb*step})
    # x max and min needs to be set as this graph utilizes that instead of labels. Max is set to one day more than the max day for the best result.
    value_dictionary['x_axis']['min'] = start_date.day
    value_dictionary['x_axis']['max'] = end_date.day
    value_dictionary['title']['text'] = _('%(team)s, %(month)s %(year)s') % {'team': team.name, 'month': start_date.strftime('%B'), 'year': year}

    return json.dumps(value_dictionary)


def team_stat_date_json(team, start_date, end_date):
    s_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    e_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)

    slice_set = TimeSlice.objects.filter(begin__range=(s_date, e_date), user__in=members_id)
    team_list_dict = {}
    counter = 0
    for mem_id in members_id:
        team_list_dict[mem_id] = {}
        team_list_dict[mem_id]['value'] = {"type": "scatter_line", "values": [], "tip": _("%(username)s<br>Time: #ygmdate:H:i#") % {'username': User.objects.get(pk=mem_id).username}, "colour": colour(counter)}
        counter += 1

    sorted_date_list = []
    w_date = s_date
    while w_date != e_date + datetime.timedelta(days=1):
        sorted_date_list.append(w_date)
        for mem_id in members_id:
            team_list_dict[mem_id][w_date]=[]
        w_date += datetime.timedelta(days=1)

    for slice in slice_set:
        if slice.slip not in team_list_dict[slice.user_id][slice.begin.date()]:
            team_list_dict[slice.user_id][slice.begin.date()].append(slice.slip)

    # in this graph we will use unix timestamps as x-values, so steps are set to 86400 (seconds) which is equal to one day.
    # we utilize the special "text":"#date:m-d#" command for labels which generates a date in format mm-dd, from the unix timestamps.
    value_dictionary = {}
    value_dictionary['elements'] = []
    value_dictionary['title'] = {"text": True, "style": "{font-size: 20px; color: #000000; text-align: center;}"}
    value_dictionary['x_axis'] = {"min": 0, "max": True, "steps": 86400, "labels": {"rotate":"vertical","steps":86400,"visible-steps":2, "text":"#date:m-d#"}}
    value_dictionary['y_axis'] = { "min": 0, "max": True, "labels": {"text":"#ygmdate:H:i#", "labels": []}}
    value_dictionary['tooltip'] = {"mouse": 1}

    max_list = [0.01]
    for date in sorted_date_list:
        for mem_id in members_id:
            i = 0
            temp_value = 0.0
            temp_value_dict = {'x': True, 'y': True}
            while i < len(team_list_dict[mem_id][date]):
                temp_value += team_list_dict[mem_id][date][i].display_days_time(date)
                i += 1
            temp_value_dict['x'] = time.mktime(date.timetuple())
            temp_value_dict['y'] = temp_value
            team_list_dict[mem_id]['value']['values'].append(temp_value_dict)
            max_list.append(temp_value)

    for mem_id in members_id:
        value_dictionary['elements'].append(team_list_dict[mem_id]['value'])

    value_dictionary['y_axis']['max'] = max(max_list) * 1.05
    step = max(max_list) * 1.05 * 0.1
    for numb in range(11):
        value_dictionary['y_axis']['labels']['labels'].append({'y': numb*step})
    value_dictionary['x_axis']['min'] = time.mktime(s_date.timetuple()) # a way to make a unix timestamp.
    value_dictionary['x_axis']['max'] = time.mktime(e_date.timetuple())
    value_dictionary['title']['text'] = _('%(team)s: From %(start)s to %(end)s') % {'team': team.name, 'start': s_date, 'end': e_date}

    return json.dumps(value_dictionary)

