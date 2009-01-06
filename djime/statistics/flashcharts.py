import datetime
from djime.models import TimeSlice
try:
    import json
except ImportError:
    import simplejson as json

def user_week_json(user, week, year):
    slice_query_set = TimeSlice.objects.filter(week_number=week, create_date__year= year, user = user.id)
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
        if slice.slip not in date_slip_dict[slice.create_date]:
            date_slip_dict[slice.create_date].append(slice.slip)
    
    # the value_dictionary, will be the dictionary that needs to be converted to json data. A lot of the data is static strings,
    # but there are 6 varibles that are different. 2 empty lists where data will be appended (values and labels list) and 4 values set to True.
    # can add a colour generator later to create colours for the graph instead of static colours.
    value_dictionary = {}
    value_dictionary['elements'] = [{"tip": "#key#<br>Time: #gmdate:H.i# Total: #totalgmdate:H.i#", "type": "bar_stack", "colours": ["#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF"], "values": []}]
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

    value_dictionary['title']['text'] = '%s Week: %s Year: %s' % (user.username, week, year)

    return json.dumps(value_dictionary)