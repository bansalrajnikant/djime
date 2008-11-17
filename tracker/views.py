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

        elif request.method == 'DELETE':
            slip.delete()
            # TODO: Send a message to the user that deltion succeeded.
            return HttpResponse('Successfully deleted slip %s' % slip.name)

        elif request.method == 'PUT':
            # TODO: Update the slip with the data from put.
            return HttpResponse('We did nothing with slip %s' % slip.name)


@login_required()
def slip_action(request, slip_id, action):
    return HttpResponseNotAllowed(('PUT',))

@login_required()
def slip_create(request):
    return HttpResponseNotAllowed(('POST',))
