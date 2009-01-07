from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from teams.forms import *
from teams.models import Team

@login_required()
def index(request):
    teams = Team.objects.filter(deleted=False, members=request.user)
    teams_member = teams.exclude(creator=request.user).order_by("name")
    teams_creator = teams.filter(creator=request.user).order_by("name")

    return render_to_response("teams/index.html", {
        "teams_member": teams_member,
        "teams_member_count": len(teams_member),
        "teams_creator": teams_creator,
        "teams_creator_count": len(teams_creator),
    }, context_instance=RequestContext(request))


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

@login_required()
def team(request, slug):
    team = get_object_or_404(Team, slug=slug)
    if team.deleted:
        raise Http404
    if request.user not in team.members.all():
        return HttpResponseForbidden('Access Denied')

    if request.method == "POST":
        if request.POST["action"] == "leave":
            team.members.remove(request.user)
            request.user.message_set.create(message="You have left the team %s" % team.name)
            return HttpResponseRedirect(reverse('team_index'))

    are_member = request.user in team.members.all()

    return render_to_response("teams/team.html", {
        "team": team,
        "are_member": are_member,
    }, context_instance=RequestContext(request))

@login_required()
def edit(request, slug, form_class=TeamUpdateForm):
    team = get_object_or_404(Team, slug=slug)
    if team.deleted:
        raise Http404
    if request.user != team.creator:
        return HttpResponseForbidden('Access Denied')

    if request.method == "POST":
        if request.POST["action"] == "update" and request.user == team.creator:
            team_form = form_class(request.POST, instance=team)
            if team_form.is_valid():
                team = team_form.save()
        else:
            team_form = form_class(instance=team)
        if request.POST["action"].split('_')[0] == 'remove':
            try:
                remove_user = User.objects.get(pk=int(request.POST["action"].split('_')[1]))
                team.members.remove(remove_user)
                request.user.message_set.create(message="User %s have been removed from your team." % remove_user.username)
                return HttpResponseRedirect(reverse('team_edit', args=(team.slug,)))
            except User.DoesNotExist:
                request.user.message_set.create(message="User does not exist.")
                return HttpResponseRedirect(reverse('team_edit', args=(team.slug,)))

    else:
        team_form = form_class(instance=team)

    are_member = request.user in team.members.all()

    return render_to_response("teams/edit.html", {
        "team_form": team_form,
        "team": team,
        "are_member": are_member,
    }, context_instance=RequestContext(request))