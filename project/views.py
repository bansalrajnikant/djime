from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.loader import render_to_string
from project.models import Project, Client
from teams.models import Team
from djime.models import Slip

def index(request):
    projects = Project.objects.all()
    return render_to_response('project/project_index.html', {'projects': projects},
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
    # Data returned to the template.
    data = {
        'project': project,
    }
    data['slip_all'] = Slip.objects.filter(project=project)
    data['slip_user'] = data['slip_all'].filter(user=request.user)
    data['slip_rest'] = data['slip_all'].exclude(user=request.user)
    duration = 0
    for slip in data['slip_all']:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    data['time_all'] ='%02i:%02i' % (duration/3600, duration%3600/60)
    duration = 0
    for slip in data['slip_user']:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    data['time_user'] ='%02i:%02i' % (duration/3600, duration%3600/60)
    duration = 0
    for slip in data['slip_rest']:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    data['time_other'] ='%02i:%02i' % (duration/3600, duration%3600/60)

    data['user_list'] = render_to_string('tracker/slip_list.html',
                              {'slip_list': data['slip_user'],
                               'list_exclude_project': True,
                              },
                              context_instance=RequestContext(request))

    data['other_list'] = render_to_string('tracker/slip_list.html',
                              {'slip_list': data['slip_rest'],
                               'list_exclude_project': True,
                              },
                              context_instance=RequestContext(request))

    return render_to_response('project/project.html', data,
                              context_instance=RequestContext(request))


@login_required()
def client_index(request):
    clients = Client.objects.all()
    return render_to_response('project/client_index.html', {'clients': clients},
                                        context_instance=RequestContext(request))


@login_required()
def show_client(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    data = {
        'client': client,
    }
    projects = Project.objects.filter(client=client, members=request.user)
    data['slip_all'] = Slip.objects.filter(project__in=projects)
    data['slip_user'] = data['slip_all'].filter(user=request.user)
    data['slip_rest'] = data['slip_all'].exclude(user=request.user)
    duration = 0
    for slip in data['slip_all']:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    data['time_all'] ='%02i:%02i' % (duration/3600, duration%3600/60)
    duration = 0
    for slip in data['slip_user']:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    data['time_user'] ='%02i:%02i' % (duration/3600, duration%3600/60)
    duration = 0
    for slip in data['slip_user']:
        seconds = 0
        for slice in slip.timeslice_set.all():
            seconds += slice.duration
        duration += seconds
    data['time_other'] ='%02i:%02i' % (duration/3600, duration%3600/60)
    
    data['user_list'] = render_to_string('tracker/slip_list.html',
                              {'slip_list': data['slip_user'],
                              'list_exclude_client': True
                              },
                              context_instance=RequestContext(request))

    data['other_list'] = render_to_string('tracker/slip_list.html',
                              {'slip_list': data['slip_rest'],
                              'list_exclude_client': True
                              },
                              context_instance=RequestContext(request))
    
    
    
    return render_to_response('project/client.html', data,
                                      context_instance=RequestContext(request))


@login_required()                                      
def show_user_clients(request, user_id, user_type):
    user_id = int(user_id)
    if user_type == 'user':
        if request.user.id != int(user_id):
            return HttpResponseForbidden('Access Denied')
        user = User.objects.get(pk=user_id)
        user.name = user.username
        projects = Project.objects.filter(members = user_id)
        clients = []
        for project in projects:
            if project.client and project.client not in clients:
                clients.append(project.client)
    elif user_type == 'team':
        user = team = get_object_or_404(Team, pk=user_id)
        if request.user not in team.members.all():
            return HttpResponseForbidden('Access Denied')
        projects = Project.objects.filter(team = user_id)
        clients = []
        for project in projects:
            if project.client and project.client not in clients:
                clients.append(project.client)
    elif user_type == 'project':
        user = project = Project.objects.get(pk=user_id)
        clients = [project.client]
    return render_to_response('project/all_user_clients.html', {'clients': clients, 'user_model': user, 'user_type': user_type},
                                      context_instance=RequestContext(request))
    
