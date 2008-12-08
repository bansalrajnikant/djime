from django.http import *
from django.db import models
import datetime
from tracker.models import Slip, TimeSlice
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from statistics.forms import DateSelectionForm

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

    form = DateSelectionForm()
    return render_to_response('statistics/date.html', {'user_id': user_id, 'form': form},
                                      context_instance=RequestContext(request))

@login_required()
def date_selection_form(request, user_id):
    if request.method not in ('POST', 'GET'):
        return HttpResponseNotAllowed('POST', 'GET')

    if request.method == 'GET':
        form = DateSelectionForm()
        return render_to_response('statistics/date_selection.html', {'user_id': user_id, 'form': form},
                                      context_instance=RequestContext(request))

    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            return HttpResponseRedirect('/statistics/user/%s/date/%s/%s/' % (user_id, start, end))
        else:
                return render_to_response('statistics/date_selection.html', {'user_id': user_id, 'form': form},
                                      context_instance=RequestContext(request))

@login_required()
def date_selection_display(request, user_id, start_date, end_date):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')


    s_date = start_date.split('-')
    e_date = end_date.split('-')
    date_diff = int(e_date[0])*365+int(e_date[1])*30+int(e_date[2])-(int(s_date[0])*365+int(s_date[1])*30+int(s_date[2]))
    if date_diff < 60 and date_diff > 0:
        return render_to_response('statistics/date_display.html', {'user_id': user_id, 'start_date': start_date, 'end_date': end_date},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponse('Invalid date, max 60 days')

def get_data(request, action, data, year, user_id):
    if request.method != 'GET':
         return HttpResponseNotAllowed('GET')

    if action == 'week':
        week = int(data)
        year = int(year)
        slice_set = TimeSlice.objects.filter(week_number=week, create_date__year= year, user = user_id)
        start_date = datetime.date(year, 1, 1) + datetime.timedelta(days = (week-2)*7)
        while start_date.isocalendar()[1] != week:
            start_date += datetime.timedelta(days=1)
        end_date = start_date + datetime.timedelta(days=6)
        w_date = start_date
        dates = {}
        while w_date != end_date:
            dates[w_date]=[]
            w_date += datetime.timedelta(days=1)
        dates[end_date] = []

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
            label += '"' + labl.strftime('%A') +'",'

        return HttpResponse('{ "elements": [ { "type": "bar_stack",'
                            '"colours": [ "#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF" ],'
                            '"values": ['+ val_all[:-1] +'],'
                            '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                            '"title": { "text": "Week ' + str(week) + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                            '"x_axis": { "labels": { "labels": [ ' + label[:-1] + '] } },'
                            '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }')


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

        slice_set = TimeSlice.objects.filter(user = user_id, create_date__range=(start_date, end_date))
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
                                '"colours": [ "#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF" ],'
                                '"values": ['+ val_all[:-1] +'],'
                                '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                                '"title": { "text": "' + start_date.strftime('%B') + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                                '"x_axis": { "labels": { "labels": [ ' + label[:-1] + '] } },'
                                '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }')


def get_date_data(request, user_id, start_date, end_date):
    # we want start and end date to have the format: u'yyyy-mm-dd'
    s_date_list = start_date.split('-')
    e_date_list = end_date.split('-')

    s_date = datetime.date(int(s_date_list[0]), int(s_date_list[1]), int(s_date_list[2]))
    e_date = datetime.date(int(e_date_list[0]), int(e_date_list[1]), int(e_date_list[2]))
    w_date = s_date
    dates = {}
    while w_date != e_date:
        dates[w_date]=[]
        w_date += datetime.timedelta(days=1)
    dates[e_date] = []

    slice_set = TimeSlice.objects.filter(user = user_id, create_date__range=(s_date, e_date))
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
                            '"colours": [ "#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF" ],'
                            '"values": ['+ val_all[:-1] +'],'
                            '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                            '"title": { "text": "From ' + str(start_date)+ ' to ' + str(end_date) + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                            '"x_axis": { "labels": { "labels": [ ' + label[:-1] + '] } },'
                            '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }')
