from django.http import HttpResponse, HttpResponseForbidden
from project.models import Project, Client
from teams.models import Team
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from tracker.models import Slip
from django.contrib.auth.models import User

def show_all_projects(request):
    projects = Project.objects.all()
    return render_to_response('project/all_projects.html', {'projects': projects},
                                         context_instance=RequestContext(request))


@login_required()
def show_user_projects(request, user_type, user_id):
    user_id = int(user_id)
    if user_type == 'user':
        if request.user.id != int(user_id):
            return HttpResponseForbidden('Access Denied')
        user = User.objects.get(pk=user_id)
        user.name = user.username
        projects = Project.objects.filter(members = user_id)
    elif user_type == 'team':
        user = team = get_object_or_404(Team, pk=user_id)
        if request.user not in team.members.all():
            return HttpResponseForbidden('Access Denied')
        projects = Project.objects.filter(team = user_id)
    elif user_type == 'client':
        user = client = get_object_or_404(Client, pk=user_id)
        projects = Project.objects.filter(client = client)
    return render_to_response('project/all_user_projects.html', {'projects': projects, 'user_model': user, 'user_type': user_type},
                                      context_instance=RequestContext(request))


@login_required()
def show_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.user not in project.members.all():
        return HttpResponseForbidden('Access Denied')
    slip_set_all = Slip.objects.filter(project=project)
    slip_set_user = slip_set_all.filter(user=request.user)
    slip_set_exclude_user = slip_set_all.exclude(user=request.user)
    duration = 0
    for slip in slip_set_all:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    time_all ='%02i:%02i' % (duration/3600, duration%3600/60)
    duration = 0
    for slip in slip_set_user:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    time_user ='%02i:%02i' % (duration/3600, duration%3600/60)
    duration = 0
    for slip in slip_set_user:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    time_other ='%02i:%02i' % (duration/3600, duration%3600/60) 
    return render_to_response('project/project.html', {'project': project, 'slip_user': slip_set_user, 'slip_rest': slip_set_exclude_user, 'slip_all': slip_set_all, 'time': time, 'time_user': time_user, 'time_other': time_other},
                                      context_instance=RequestContext(request))


def show_all_clients(request):
    clients = Client.objects.all()
    return render_to_response('project/all_clients.html', {'clients': clients},
                                        context_instance=RequestContext(request))


def show_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    #if request.user not in client.members.all():
        #return HttpResponseForbidden('Access Denied')
    slip_set_all = Slip.objects.filter(client=client)
    slip_set_user = slip_set_all.filter(user=request.user)
    slip_set_exclude_user = slip_set_all.exclude(user=request.user)
    duration = 0
    for slip in slip_set_all:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    time ='%02i:%02i' % (duration/3600, duration%3600/60)
    return render_to_response('project/client.html', {'client': client, 'slip_user': slip_set_user, 'slip_rest': slip_set_exclude_user, 'slip_all': slip_set_all, 'time': time},
                                      context_instance=RequestContext(request))