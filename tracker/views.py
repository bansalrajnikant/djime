from django.http import *
from django.shortcuts import render_to_response, get_object_or_404
from djime.tracker.models import Slip, TimeSlice
from django.contrib.auth.decorators import login_required
from django.template import RequestContext


def index(request):
    return render_to_response('tracker/index.html', {},
                              context_instance=RequestContext(request))


@login_required()
def slip(request, slip_id):
    valid_methods = ('GET', 'PUT', 'DELETE')

    if request.method not in valid_methods:
        return HttpResponseNotAllowed(('GET', 'PUT', 'DELETE'))
    else:
        slip = get_object_or_404(Slip, pk=slip_id)
        if request.user != slip.user:
            return HttpResponseForbidden('Access denied')

        if request.method == 'GET':
            return render_to_response('tracker/slip.html', {'slip': slip},
                                      context_instance=RequestContext(request))



def slip_action(request, slip_id, action):
    return HttpResponseNotAllowed(('PUT',))

def slip_create(request):
    return HttpResponseNotAllowed(('POST',))
