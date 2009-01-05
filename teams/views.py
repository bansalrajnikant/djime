from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from teams.forms import *
from teams.models import Team

def create(request, form_class=TeamForm, template_name="teams/create.html"):
    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "create":
            team_form = form_class(request.POST)
            if team_form.is_valid():
                team = team_form.save(commit=False)
                team.creator = request.user
                team.save()
                team.members.add(request.user)
                team.save()
                return HttpResponseRedirect(team.get_absolute_url())
        else:
            team_form = form_class()
    else:
        team_form = form_class()

    return render_to_response(template_name, {
        "team_form": team_form,
    }, context_instance=RequestContext(request))


def delete(request, slug, redirect_url=None):
    team = get_object_or_404(Team, slug=slug)
    if not redirect_url:
        redirect_url = "/teams/" # @@@ can't use reverse("teams") -- what is URL name using things?

    # @@@ eventually, we'll remove restriction that team.creator can't leave team but we'll still require team.members.all().count() == 1
    if request.user.is_authenticated() and request.method == "POST" and request.user == team.creator and team.members.all().count() == 1:
        team.deleted = True
        team.save()
        request.user.message_set.create(message="Team %s deleted." % team)
        # @@@ no notification as the deleter must be the only member

    return HttpResponseRedirect(redirect_url)


def your_teams(request, template_name="teams/your_teams.html"):
    return render_to_response(template_name, {
        "teams": Team.objects.filter(deleted=False, members=request.user).order_by("name"),
    }, context_instance=RequestContext(request))
your_teams = login_required(your_teams)

def team(request, slug, form_class=TeamUpdateForm,
        template_name="teams/team.html"):
    team = get_object_or_404(Team, slug=slug)

    if team.deleted:
        raise Http404

    if request.user.is_authenticated() and request.method == "POST":
        if request.POST["action"] == "update" and request.user == team.creator:
            team_form = form_class(request.POST, instance=team)
            if team_form.is_valid():
                team = team_form.save()
        else:
            team_form = form_class(instance=team)
        if request.POST["action"] == "join":
            team.members.add(request.user)
            request.user.message_set.create(message="You have joined the team %s" % team.name)
        elif request.POST["action"] == "leave":
            team.members.remove(request.user)
            request.user.message_set.create(message="You have left the team %s" % team.name)
    else:
        team_form = form_class(instance=team)

    are_member = request.user in team.members.all()

    return render_to_response(template_name, {
        "team_form": team_form,
        "team": team,
        "are_member": are_member,
    }, context_instance=RequestContext(request))
