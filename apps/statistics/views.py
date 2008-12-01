from django.http import *
from django.db import models
import datetime
from tracker.models import Slip, TimeSlice
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required()
def todays_week(request, user_id):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')
    else:
        week = datetime.datetime.now().isocalendar()[1]
        year = datetime.datetime.now().isocalendar()[0]
        return render_to_response('statistics/week.html', {'week' : week, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))


@login_required()
def week(request, user_id, year, week):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')


    return render_to_response('statistics/week.html', {'week': week, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))


@login_required()
def todays_month(request, user_id):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    return render_to_response('statistics/month.html', {'month' : month, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))


@login_required()
def month(request, user_id, year, month):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')

    return render_to_response('statistics/month.html', {'month' : month, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))

@login_required()
def date(request, user_id):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')

    return render_to_response('statistics/date.html', {'user_id': user_id},
                                      context_instance=RequestContext(request))


def get_data(request, action, data, year, user_id):
    if request.method != 'GET':
         return HttpResponseNotAllowed('GET')

    if action == 'week':
        week = data
        slice_set = TimeSlice.objects.filter(week_number=week, year = year, user = user_id)
        monday = []
        tuesday = []
        wednesday = []
        thursday = []
        friday = []
        saturday = []
        sunday =  []
        names = []
        times = []
        monday_date = tuesday_date = wednesday_date = thursday_date = friday_date = saturday_date = sunday_date = ''

        for slice in slice_set:
            if slice.begin.weekday() == 0:
                if slice.slip not in monday:
                    monday.append(slice.slip)
                    monday_date = slice.create_date
            elif slice.begin.weekday() == 1:
                if slice.slip not in tuesday:
                    tuesday.append(slice.slip)
                    tuesday_date = slice.create_date
            elif slice.begin.weekday() == 2:
                if slice.slip not in wednesday:
                    wednesday.append(slice.slip)
                    wednesday_date = slice.create_date
            elif slice.begin.weekday() == 3:
                if slice.slip not in thursday:
                    thursday.append(slice.slip)
                    thursday_date = slice.create_date
            elif slice.begin.weekday() == 4:
                if slice.slip not in friday:
                    friday.append(slice.slip)
                    friday_date = slice.create_date
            elif slice.begin.weekday() == 5:
                if slice.slip not in saturday:
                    saturday.append(slice.slip)
                    saturday_date = slice.create_date
            else:
                if slice.slip not in sunday:
                    sunday.append(slice.slip)
                    sunday_date = slice.create_date


        week_days = [ monday, tuesday, wednesday, thursday, friday, saturday, sunday]
        j = 0
        date = monday_date
        for day in week_days:
            i=0
            temp = ''
            temp_max = 0.0
            while i < len(day):
                if not temp:
                    temp += '['
                temp += '{ "val" :' + day[i].display_days_time(date) + ', "tip": "' + day[i].name + '<br>day: #x_label#<br>time: #val# total: #total#"}'
                temp_max += float(day[i].display_days_time(date))
                if i != len(day)-1:
                    temp += ','
                if i == len(day)-1:
                    temp += ']'
                i += 1
            if not temp:
                temp = '[0]'
            if j == 0:
                monday_val = temp
                mon_max = temp_max
                date = tuesday_date
            elif j == 1:
                tuesday_val = temp
                tue_max = temp_max
                date = wednesday_date
            elif j == 2:
                date = thursday_date
                wednesday_val = temp
                wed_max = temp_max
            elif j == 3:
                date = friday_date
                thursday_val = temp
                thur_max = temp_max
            elif j == 4:
                date = saturday_date
                friday_val = temp
                fri_max = temp_max
            elif j == 5:
                date = sunday_date
                saturday_val = temp
                sat_max = temp_max
            else:
                sunday_val = temp
                sun_max = temp_max
            j +=1




        max_val = max(mon_max, tue_max, wed_max, thur_max, fri_max, sat_max, sun_max)
        step = max_val/10


        return HttpResponse('{ "elements": [ { "type": "bar_stack",'
                            '"colours": [ "#F00000", "#FFFF00", "#300030", "#000000", "#D54C78", "#D54C78" ],'
                            '"values": ['+ monday_val + ',' + tuesday_val + ',' + wednesday_val + ',' + thursday_val + ',' + friday_val + ',' + saturday_val + ',' + sunday_val +']} ],'
                            '"title": { "text": "Year '+str(year)+' Week ' + str(week) + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                            '"bg_colour": "#FEFEFE",'
                            '"x_axis": { "labels": { "labels": [ "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" ] } },'
                            '"y_axis": {    "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }')

    if action == 'month':
        month = int(data)
        year = int(year)
        start_date = datetime.date(year, month, 1)
        end_date = start_date + datetime.timedelta(days=30)
        while end_date.month != start_date.month:
            end_date -= datetime.timedelta(days=1)

        w_date = start_date
        dates = {}
        while w_date != end_date:
            dates[w_date]=[]
            w_date += datetime.timedelta(days=1)
        dates[end_date] = []

        slice_set = TimeSlice.objects.filter(user = user_id, create_date__gte=start_date, create_date__lte=end_date)
        for slice in slice_set:
            if slice.slip not in dates[slice.create_date]:
                dates[slice.create_date].append(slice.slip)

        max_list = [0.01]
        for date in dates.keys():
            i=0
            temp = ''
            temp_max = 0.0
            while i < len(dates[date]):
                if not temp:
                    temp += '['
                temp += '{ "val" :' + dates[date][i].display_days_time(date) + ', "tip": "' + dates[date][i].name + '<br> time: #val# total: #total#"}'
                temp_max += float(dates[date][i].display_days_time(date))
                if i != len(dates[date])-1:
                    temp += ','
                if i == len(dates[date])-1:
                    temp += ']'
                i += 1
            if not temp:
                temp = '[0]'
            dates[date] = temp
            max_list.append(temp_max)

        max_val = max(max_list)
        step = max_val*0.1
        label_list = []

        for key in dates.keys():
            label_list.append(key)

        label_list.sort()

        val_all = ''
        for sorted_date in label_list:
            val_all += dates[sorted_date] + ','

        label = ''
        for labl in label_list:
            label += '"' + str(labl.day) +'",'

        return HttpResponse('{ "elements": [ { "type": "bar_stack",'
                                '"colours": [ "#F00000", "#FF0000", "#FFF000", "#FFFF00", "#FFFFF0", "#FFFFFF" ],'
                                '"values": ['+ val_all[:-1] +'],'
                                '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                                '"title": { "text": "From ' + str(start_date)+ ' to ' + str(end_date) + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                                '"x_axis": { "labels": { "labels": [ ' + label[:-1] + '] } },'
                                '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }')


def get_date_data(request, user_id, start_date, end_date):
    # we want start and end date to be lists: [yyyy, mm, dd]:

    s_date = datetime.date(start_date[0], start_date[1], start_date[2])
    e_date = datetime.date(end_date[0], end_date[1], end_date[2])
    w_date = s_date
    dates = {}
    while w_date != e_date:
        dates[w_date]=[]
        w_date += datetime.timedelta(days=1)
    dates[e_date] = []

    slice_set = TimeSlice.objects.filter(user = user_id, create_date__gte=s_date, create_date__lte=e_date)
    for slice in slice_set:
        if slice.slip not in dates[slice.create_date]:
            dates[slice.create_date].append(slice.slip)

    max_list = [0.01]
    for date in dates.keys():
        i=0
        temp = ''
        temp_max = 0.0
        while i < len(dates[date]):
            if not temp:
                temp += '['
            temp += '{ "val" :' + dates[date][i].display_days_time(date) + ', "tip": "' + dates[date][i].name + '<br> time: #val# total: #total#"}'
            temp_max += float(dates[date][i].display_days_time(date))
            if i != len(dates[date])-1:
                temp += ','
            if i == len(dates[date])-1:
                temp += ']'
            i += 1
        if not temp:
            temp = '[0]'
        dates[date] = temp
        max_list.append(temp_max)

    max_val = max(max_list)
    step = max_val*0.1

    label_list = []

    for key in dates.keys():
        label_list.append(key)

    label_list.sort()

    val_all = ''
    for sorted_date in label_list:
        val_all += dates[sorted_date] + ','

    label = ''
    for labl in label_list:
        label += '"' + str(labl.day) +'",'

    return HttpResponse('{ "elements": [ { "type": "bar_stack",'
                            '"colours": [ "#F00000", "#FF0000", "#FFF000", "#FFFF00", "#FFFFF0", "#FFFFFF" ],'
                            '"values": ['+ val_all[:-1] +'],'
                            '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                            '"title": { "text": "From ' + str(start_date)+ ' to ' + str(end_date) + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                            '"x_axis": { "labels": { "labels": [ ' + label[:-1] + '] } },'
                            '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }')
