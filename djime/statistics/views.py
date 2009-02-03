import datetime
from django.contrib.auth.decorators import login_required
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from djime.statistics.forms import DateSelectionForm
from teams.models import Team
import djime.statistics.flashcharts as flashcharts
from django.utils.translation import ugettext as trans

@login_required()
def index(request):
    return render_to_response('statistics/index.html', {},
                              context_instance=RequestContext(request))


@login_required()
def display_user_week(request, user_id, year, week):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden(trans('Access denied'))
    return render_to_response('statistics/display_user_week.html', {'week': week, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))


@login_required()
def display_user_month(request, user_id, year, month):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden(trans('Access denied'))
    return render_to_response('statistics/display_user_month.html', {'month' : month, 'year': year, 'user_id': user_id},
                                      context_instance=RequestContext(request))


@login_required()
def user_date_selection_form(request, user_id):
    if request.method not in ('POST', 'GET'):
        return HttpResponseNotAllowed('POST', 'GET')

    if request.method == 'GET':
        form = DateSelectionForm()
        return render_to_response('statistics/user_date_selection.html', {'user_id': user_id, 'form': form},
                                      context_instance=RequestContext(request))

    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            return HttpResponseRedirect('/statistics/user/%s/date/%s/%s/' % (user_id, start, end))
        else:
            return render_to_response('statistics/user_date_selection.html', {'user_id': user_id, 'form': form},
                                      context_instance=RequestContext(request))


@login_required()
def display_user_date_selection(request, user_id, start_date, end_date):
    if int(request.user.id) != int(user_id):
        return HttpResponseForbidden('Access denied')
    s_date = start_date.split('-')
    e_date = end_date.split('-')
    date_diff = int(e_date[0])*365+int(e_date[1])*30+int(e_date[2])-(int(s_date[0])*365+int(s_date[1])*30+int(s_date[2]))
    if date_diff < 60 and date_diff > 0:
        return render_to_response('statistics/display_user_date.html', {'user_id': user_id, 'start_date': start_date, 'end_date': end_date},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponse(trans('Invalid date, max 60 days'))


@login_required()
def display_team_week(request, team_id, year, week):
    team = get_object_or_404(Team, pk=int(team_id))
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    if request.user.id not in members_id:
        return HttpResponseForbidden(trans('Access denied'))

    return render_to_response('statistics/display_team_week.html', {'week': week, 'year': year, 'team_id': team_id},
                                      context_instance=RequestContext(request))


@login_required()
def display_team_month(request, team_id, year, month):
    team = get_object_or_404(Team, pk=int(team_id))
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    if request.user.id not in members_id:
        return HttpResponseForbidden(trans('Access denied'))

    return render_to_response('statistics/display_team_month.html', {'month' : month, 'year': year, 'team_id': team_id},
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
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            return HttpResponseRedirect('/statistics/team/%s/date/%s/%s/' % (team_id, start, end))
        else:
            return render_to_response('statistics/team_date_selection.html', {'team_id': team_id, 'form': form},
                                      context_instance=RequestContext(request))


@login_required()
def display_team_date_selection(request, team_id, start_date, end_date):
    team = get_object_or_404(Team, pk=int(team_id))
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    if request.user.id not in members_id:
        return HttpResponseForbidden(trans('Access denied'))

    s_date = start_date.split('-')
    e_date = end_date.split('-')
    date_diff = int(e_date[0])*365+int(e_date[1])*30+int(e_date[2])-(int(s_date[0])*365+int(s_date[1])*30+int(s_date[2]))
    if date_diff < 60 and date_diff > 0:
        return render_to_response('statistics/display_team_date.html', {'team_id': team_id, 'start_date': start_date, 'end_date': end_date},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponse(trans('Invalid date, max 60 days'))


@login_required()
def display_team_stat_week(request, team_id, week, year):
    team = get_object_or_404(Team, pk=int(team_id))
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    if request.user.id not in members_id:
        return HttpResponseForbidden(trans('Access denied'))

    return render_to_response('statistics/display_team_stat_week.html', {'week': week, 'year': year, 'team_id': team_id},
                                      context_instance=RequestContext(request))


@login_required()
def display_team_stat_month(request, team_id, month, year):
    team = get_object_or_404(Team, pk=int(team_id))
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    if request.user.id not in members_id:
        return HttpResponseForbidden(trans('Access denied'))

    return render_to_response('statistics/display_team_stat_month.html', {'month': month, 'year': year, 'team_id': team_id},
                                      context_instance=RequestContext(request))


@login_required()
def team_stat_date_selection_form(request, team_id):
    if request.method not in ('POST', 'GET'):
        return HttpResponseNotAllowed('POST', 'GET')

    if request.method == 'GET':
        form = DateSelectionForm()
        return render_to_response('statistics/team_stat_date_selection.html', {'team_id': team_id, 'form': form},
                                      context_instance=RequestContext(request))

    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            start = form.cleaned_data['start']
            end = form.cleaned_data['end']
            return HttpResponseRedirect('/statistics/team_stat/%s/date/%s/%s/' % (team_id, start, end))
        else:
            return render_to_response('statistics/team_stat_date_selection.html', {'team_id': team_id, 'form': form},
                                      context_instance=RequestContext(request))


@login_required()
def display_team_stat_date_selection(request, team_id, start_date, end_date):
    team = get_object_or_404(Team, pk=int(team_id))
    members = team.members.all()
    members_id = []
    for member in members:
        members_id.append(member.id)
    if request.user.id not in members_id:
        return HttpResponseForbidden(trans('Access denied'))

    s_date = start_date.split('-')
    e_date = end_date.split('-')
    date_diff = int(e_date[0])*365+int(e_date[1])*30+int(e_date[2])-(int(s_date[0])*365+int(s_date[1])*30+int(s_date[2]))
    if date_diff < 60 and date_diff > 0:
        return render_to_response('statistics/display_team_stat_date.html', {'team_id': team_id, 'start_date': start_date, 'end_date': end_date},
                                      context_instance=RequestContext(request))
    else:
        return HttpResponse(trans('Invalid date, max 60 days'))


def data_user_week(request, week, year, user_id):
    if request.method != 'GET':
         return HttpResponseNotAllowed('GET')

    week = int(week)
    year = int(year)
    return HttpResponse(flashcharts.user_week_json(request.user, week, year))


def data_user_month(request, month, year, user_id):
    if request.method != 'GET':
         return HttpResponseNotAllowed('GET')

    month = int(month)
    year = int(year)
    return HttpResponse(flashcharts.user_month_json(request.user, month, year))


def data_user_date(request, user_id, start_date, end_date):
    return HttpResponse(flashcharts.user_date_json(request.user, start_date, end_date))


def data_team_week(request, week, year, team_id):
    # this method is the same as user.
    if request.method != 'GET':
         return HttpResponseNotAllowed('GET')

    week = int(week)
    year = int(year)
    team = get_object_or_404(Team, pk=int(team_id))
    return HttpResponse(flashcharts.team_week_json(team, week, year))


def data_team_month(request, month, year, team_id):
    if request.method != 'GET':
         return HttpResponseNotAllowed('GET')

    month = int(month)
    year = int(year)
    team = get_object_or_404(Team, pk=int(team_id))
    return HttpResponse(flashcharts.team_month_json(team, month, year))


def data_team_date(request, team_id, start_date, end_date):
    team = get_object_or_404(Team, pk=int(team_id))
    return HttpResponse(flashcharts.team_date_json(team, start_date, end_date))


def data_team_stat_week(request, team_id, week, year):
    week = int(week)
    year = int(year)
    team = get_object_or_404(Team, pk=int(team_id))
    return HttpResponse(flashcharts.team_stat_week_json(team, week, year))


def data_team_stat_month(request, team_id, month, year):
    team = get_object_or_404(Team, pk=int(team_id))
    month = int(month)
    year = int(year)
    return HttpResponse(flashcharts.team_stat_month_json(team, month, year))


def data_team_stat_date(request, team_id, start_date, end_date):
    team = get_object_or_404(Team, pk=int(team_id))
    return HttpResponse(flashcharts.team_stat_date_json(team, start_date, end_date))