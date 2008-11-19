from django.http import *
from django.shortcuts import render_to_response, get_object_or_404
from djime.tracker.models import Slip, TimeSlice
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User


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
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))

    if action == 'start':
        startTime = request.POST['begin']
        newTimeSlice = TimeSlice.objects.create(user = request.user, begin = startTime, slip_id = slip_id )
        newTimeSlice.save()
        return HttpResponse('Your timeslice begin time %s has been created' % startTime)

    elif action == 'stop':
        getTimeSlice = TimeSlice.objects.get(user = request.user, slip = slip_id, end = None)
        getTimeSlice.end = request.POST['end']
        getTimeSlice.save()
        return HttpResponse('Your timeslice for slip "%s", begintime %s has been stopped at %s' % (getTimeSlice.slip.name, getTimeSlice.begin, getTimeSlice.end))
    else:
        #Make a return for only action allowed is start/stop
        pass

@login_required()
def slip_create(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))
    name = request.POST['name']
    newSlip = Slip.objects.create(user = request.user, name = name)
    newSlip.save()
    return HttpResponse('Your slip "%s" has been created' % name)
