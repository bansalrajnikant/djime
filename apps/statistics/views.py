from django.http import *
from django.db import models
import datetime
from tracker.models import Slip, TimeSlice
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from statistics.forms import DateSelectionForm, DateSelectionBetaForm
from teams.models import Team
from statistics.colour import Colour

@login_required()
def todays_week(request, search, search_id):
    if search == 'user':
        if int(request.user.id) != int(search_id):
            return HttpResponseForbidden('Access denied')
    elif search == 'team':
        team = get_object_or_404(Team, pk=int(search_id))
        members = team.members.all()
        members_id = []
        for member in members:
            members_id.append(member.id)
        if request.user.id not in members_id:
            return HttpResponseForbidden('Access denied')

    week = datetime.datetime.now().isocalendar()[1]
    year = datetime.datetime.now().isocalendar()[0]
    return render_to_response('statistics/week.html', {'week' : week, 'year': year, 'search': search, 'search_id': search_id},
                                  context_instance=RequestContext(request))


@login_required()
def week(request, search, search_id, year, week):
    if search == 'user':
        if int(request.user.id) != int(search_id):
            return HttpResponseForbidden('Access denied')
    elif search == 'team':
        team = get_object_or_404(Team, pk=int(search_id))
        members = team.members.all()
        members_id = []
        for member in members:
            members_id.append(member.id)
        if request.user.id not in members_id:
            return HttpResponseForbidden('Access denied')


    return render_to_response('statistics/week.html', {'week': week, 'year': year, 'search': search, 'search_id': search_id},
                                      context_instance=RequestContext(request))


@login_required()
def todays_month(request, search, search_id):
    if search == 'user':
        if int(request.user.id) != int(search_id):
            return HttpResponseForbidden('Access denied')
    elif search == 'team':
        team = get_object_or_404(Team, pk=int(search_id))
        members = team.members.all()
        members_id = []
        for member in members:
            members_id.append(member.id)
        if request.user.id not in members_id:
            return HttpResponseForbidden('Access denied')

    month = datetime.datetime.now().month
    year = datetime.datetime.now().year
    return render_to_response('statistics/month.html', {'month' : month, 'year': year, 'search': search, 'search_id': search_id},
                                      context_instance=RequestContext(request))


@login_required()
def month(request, search, search_id, year, month):
    if search == 'user':
        if int(request.user.id) != int(search_id):
            return HttpResponseForbidden('Access denied')
    elif search == 'team':
        team = get_object_or_404(Team, pk=int(search_id))
        members = team.members.all()
        members_id = []
        for member in members:
            members_id.append(member.id)
        if request.user.id not in members_id:
            return HttpResponseForbidden('Access denied')

    return render_to_response('statistics/month.html', {'month' : month, 'year': year, 'search': search, 'search_id': search_id},
                                      context_instance=RequestContext(request))

@login_required()
def date(request, search, search_id):
    if search == 'user':
        if int(request.user.id) != int(search_id):
            return HttpResponseForbidden('Access denied')
    elif search == 'team':
        team = get_object_or_404(Team, pk=int(search_id))
        members = team.members.all()
        members_id = []
        for member in members:
            members_id.append(member.id)
        if request.user.id not in members_id:
            return HttpResponseForbidden('Access denied')


    week = datetime.datetime.now().isocalendar()[1]
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    form = DateSelectionForm()
    form_beta = DateSelectionBetaForm()
    return render_to_response('statistics/date.html', {'search': search, 'search_id': search_id, 'form': form, 'team_id': search_id, 'form_beta': form_beta, 'week': week, 'month': month, 'year': year},
                                      context_instance=RequestContext(request))

@login_required()
def date_selection_form(request, search, search_id):
    if request.method not in ('POST', 'GET'):
        return HttpResponseNotAllowed('POST', 'GET')

    if request.method == 'GET':
        form = DateSelectionForm()
        return render_to_response('statistics/date_selection.html', {'search': search, 'search_id': search_id, 'form': form},
                                      context_instance=RequestContext(request))

    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            return HttpResponseRedirect('/statistics/%s/%s/date/%s/%s/' % (search, search_id, start, end))
        else:
            return render_to_response('statistics/date_selection.html', {'search': search, 'search_id': search_id, 'form': form},
                                      context_instance=RequestContext(request))


@login_required()
def team_date_selection_form(request, team_id):
    if request.method not in ('POST', 'GET'):
        return HttpResponseNotAllowed('POST', 'GET')

    if request.method == 'GET':
        form = DateSelectionForm()
        return render_to_response('statistics/team_date_selection.html', {'team_id': team_id, 'form': form},
                                      context_instance=RequestContext(request))

    if request.method == 'POST':
        form = DateSelectionBetaForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            return HttpResponseRedirect('/statistics/team_stat/%s/date/%s/%s/' % (team_id, start, end))
        else:
            return render_to_response('statistics/team_date_selection.html', {'team_id': team_id, 'form': form},
                                      context_instance=RequestContext(request))

@login_required()
def date_selection_display(request, search, search_id, start_date, end_date):
    if search == 'user':
        if int(request.user.id) != int(search_id):
            return HttpResponseForbidden('Access denied')
    elif search == 'team':
        team = get_object_or_404(Team, pk=int(search_id))
        members = team.members.all()
        members_id = []
        for member in members:
            members_id.append(member.id)
        if request.user.id not in members_id:
            return HttpResponseForbidden('Access denied')

    s_date = start_date.split('-')
    e_date = end_date.split('-')
    date_diff = int(e_date[0])*365+int(e_date[1])*30+int(e_date[2])-(int(s_date[0])*365+int(s_date[1])*30+int(s_date[2]))
    if date_diff < 60 and date_diff > 0:
        return render_to_response('statistics/date_display.html', {'search': search, 'search_id': search_id, 'start_date': start_date, 'end_date': end_date},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponse('Invalid date, max 60 days')


@login_required()
def team_date_selection_display(request, team_id, start_date, end_date):
    team = get_object_or_404(Team, pk=int(team_id))
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    if request.user.id not in members_id:
        return HttpResponseForbidden('Access denied')

    s_date = start_date.split('-')
    e_date = end_date.split('-')
    date_diff = int(e_date[0])*365+int(e_date[1])*30+int(e_date[2])-(int(s_date[0])*365+int(s_date[1])*30+int(s_date[2]))
    if date_diff < 60 and date_diff > 0:
        return render_to_response('statistics/team_date_display.html', {'team_id': team_id, 'start_date': start_date, 'end_date': end_date},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponse('Invalid date, max 60 days')


@login_required()
def show_team_week(request, team_id, week, year):
    team = get_object_or_404(Team, pk=int(team_id))
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    if request.user.id not in members_id:
        return HttpResponseForbidden('Access denied')


    return render_to_response('statistics/team_week.html', {'week': week, 'year': year, 'team_id': team_id},
                                      context_instance=RequestContext(request))


@login_required()
def show_team_month(request, team_id, month, year):
    team = get_object_or_404(Team, pk=int(team_id))
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    if request.user.id not in members_id:
        return HttpResponseForbidden('Access denied')

    return render_to_response('statistics/team_month.html', {'month': month, 'year': year, 'team_id': team_id},
                                      context_instance=RequestContext(request))


def get_data(request, action, data, year, search, search_id):
    if request.method != 'GET':
         return HttpResponseNotAllowed('GET')

    if action == 'week': #this will give the data for a graph for a week
        week = int(data)
        year = int(year)

        # 2 cases either get all timeslices for this week that a user or team has created
        if search == 'user':
            slice_set = TimeSlice.objects.filter(week_number=week, create_date__year= year, user = search_id)
        elif search == 'team':
            # first get a list with user ids for the team, and then use the "user__in = list" filter method
            team = get_object_or_404(Team, pk=int(search_id))
            members = team.members.all()
            members_id = []
            for member in members:
                members_id.append(member.id)
            slice_set = TimeSlice.objects.filter(week_number=week, create_date__year= year, user__in = members_id)

        # start date is set to a day in the week before the week we want to search.
        start_date = datetime.date(year, 1, 1) + datetime.timedelta(days = (week-2)*7)
        # this while loop will keep adding a day to the start date, until first day of the week is reached
        # thus start_date with be the first day of the week
        while start_date.isocalendar()[1] != week:
            start_date += datetime.timedelta(days=1)

        end_date = start_date + datetime.timedelta(days=6)
        w_date = start_date
        dates = {}

        # this while loop generates every day every day except the last in the time period
        # and adds that day in the dates dictionary
        while w_date != end_date:
            dates[w_date]=[]
            w_date += datetime.timedelta(days=1)
        dates[end_date] = []

        # this loop checks to see if a given slip of a timeslice is added to the list of that day.
        # if it hasn't been added yet it adds it to the list of slips containing timeslices made that day.
        for slice in slice_set:
            if slice.slip not in dates[slice.create_date]:
                dates[slice.create_date].append(slice.slip)

        max_list = [0.01] # will hold the max duration values needed for scaling the y-axis, lowest is set to 0.01
        # this loop will run though every day in the dates dictionary.
        for date in dates.keys():
            i=0
            temp = '' #used to store values to be put into the values list
            temp_max = 0.0
            #this while loop, will take out.
            while i < len(dates[date]):
                if not temp: #if this holds true, temp is empty (= '') and needs to get the starting bracket
                    temp += '['
                # below is added '{ "val": [duration of timeslices on slip], "tip": "[slip.name] '<br> time: #val# total: #total#"}'
                # this generates the value (val) and the tooltip (tip)
                temp += '{ "val" :' + dates[date][i].display_days_time(date) + ', "tip": "' + dates[date][i].name + '<br> time: #val# total: #total#"}'
                temp_max += float(dates[date][i].display_days_time(date)) # here every slip's duration is summed up.
                if i != len(dates[date])-1: # this adds a , between {} but not after the last
                    temp += ','
                if i == len(dates[date])-1: #when true, the last value has been added and ending ] is placed.
                    temp += ']'
                i += 1
            if not temp: #if not value has been added to temp, no timeslices was made that day, so temp = [0] equals to no values
                temp = '[0]'
            dates[date] = temp #here the value used to generate the temp value is replaces, to now hold the value used to display the graph
            max_list.append(temp_max)

        max_val = max(max_list)
        step = max_val*0.1

        #below is generated a sorted list containing all dates used.
        label_list = []
        for key in dates.keys():
            label_list.append(key)
        label_list.sort()

        val_all = ''
        for sorted_date in label_list:
            val_all += dates[sorted_date] + ','

        #below is generated the labels for the x-axis, as this only a week we will display the day names
        # using strftime. Only use label[:-1] to avoid the last ',' being added and causing syntax error in the data display format.
        label = ''
        for labl in label_list:
            label += '"' + labl.strftime('%A') +'",'

        if search == 'user':
            title = request.user.username + ' Week ' + str(week)
        elif search == 'team':
            title = Team.objects.get(pk = int(search_id)).name + ' Week ' + str(week)


        return HttpResponse(    '{ "elements": [ { "type": "bar_stack",'
                                '"colours": [ "#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF" ],'
                                '"values": ['+ val_all[:-1] +'],'
                                '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                                '"title": { "text": "'+title + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                                '"x_axis": { "labels": { "labels": [ ' + label[:-1] + '] } },'
                                '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }'
                            )


    if action == 'month':
        #this action is basicly the same as week, only start date can be found getting day 1 of the chosen month and year.
        # the end day is gotten by either getting it in the long month by adding 30 days or in the short months subtracking days in a while loop
        # until a day in the chosen month is gotten which is the last day of that month.
        # also the labels is a bit different showing day numbers instead of weeknames.
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

        if search == 'user':
            slice_set = TimeSlice.objects.filter(user = int(search_id), create_date__range=(start_date, end_date))
        elif search == 'team':
            team = get_object_or_404(Team, pk=int(search_id))
            members = team.members.all()
            members_id = []
            for member in members:
                members_id.append(member.id)
            slice_set = TimeSlice.objects.filter(user__in = members_id, create_date__range=(start_date, end_date))

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

        if search == 'user':
            title = request.user.username + ' ' + start_date.strftime('%B') + ' ' + str(year)
        elif search == 'team':
            title = Team.objects.get(pk = int(search_id)).name + ' ' + start_date.strftime('%B') + ' ' + str(year)


        return HttpResponse(    '{ "elements": [ { "type": "bar_stack",'
                                '"colours": [ "#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF" ],'
                                '"values": ['+ val_all[:-1] +'],'
                                '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                                '"title": { "text": "' + title + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                                '"x_axis": { "labels": { "labels": [ ' + label[:-1] + '] } },'
                                '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }'
                            )


def get_date_data(request, search, search_id, start_date, end_date):
    # the method is again the same.


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

    if search == 'user':
        slice_set = TimeSlice.objects.filter(user = search_id, create_date__range=(s_date, e_date))
    elif search == 'team':
        team = get_object_or_404(Team, pk=int(search_id))
        members = team.members.all()
        members_id = []
        for member in members:
            members_id.append(member.id)
        slice_set = TimeSlice.objects.filter(user__in = members_id, create_date__range=(s_date, e_date))

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

    if search == 'user':
            title = request.user.username + ' ' + str(start_date)+ ' to ' + str(end_date)
    elif search == 'team':
        title = Team.objects.get(pk = int(search_id)).name + ' ' + str(start_date)+ ' to ' + str(end_date)



    return HttpResponse(    '{ "elements": [ { "type": "bar_stack",'
                            '"colours": [ "#FF0000", "#0000FF", "#00FF00", "#FFFF00", "#FF00FF", "#00FFFF", "#000000", "#FFFFFF" ],'
                            '"values": ['+ val_all[:-1] +'],'
                            '"tip": "#y_label# X label [#x_label#], Value [#val#] Total [#total#]" } ],'
                            '"title": { "text": "' + title + '" , "style": "{font-size: 20px; color: #F24062; text-align: center;}" },'
                            '"x_axis": { "labels": { "labels": [ ' + label[:-1] + '] } },'
                            '"y_axis": {  "min": 0, "max": '+str(max_val)+', "steps": '+str(step)+' }, "tooltip": { "mouse": 2 } }'
                        )
