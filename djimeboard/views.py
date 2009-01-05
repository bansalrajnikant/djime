"""
Djimeboard provides a simple dashboard, used as the starting page for
the user. It's supposed to provide a quick overview of all the users
activities in Djime without to much visual noise.
"""

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from tracker.models import Slip, TimeSlice
from project.models import Client, Project

@login_required()
def index(request):
    display_data = {
        'slip_list': Slip.objects.filter(user=request.user)[:10],
        'project_list': Project.objects.all()[:10],
    }
    return render_to_response('djimeboard/index.html', display_data,
                              context_instance=RequestContext(request))
    
