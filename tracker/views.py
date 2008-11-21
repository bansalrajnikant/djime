from django.http import *
from django.shortcuts import render_to_response, get_object_or_404
from djime.tracker.models import Slip, TimeSlice
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from datetime import datetime


def index(request):
    return render_to_response('tracker/index.html', {},
                              context_instance=RequestContext(request))

@login_required()
def slip(request, slip_id):
    valid_methods = ('GET', 'POST', 'DELETE')

    if request.method not in valid_methods:
        return HttpResponseNotAllowed(('GET', 'POST', 'DELETE'))
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

        elif request.method == 'POST':
            slip = Slip.objects.get(id = slip_id)
            old_name = slip.name
            slip.name = request.POST['name']
            slip.save()
            return HttpResponse("We changed the slip's name from '%s' to '%s'" % (old_name, slip.name))


@login_required()
def slip_action(request, slip_id, action):
    if request.method not in ('GET', 'POST'):
        return HttpResponseNotAllowed(('POST', 'GET'))

    if action == 'start':
        if request.POST.has_key('begin'):
            start_time = request.POST['begin']
        else:
            start_time = datetime.now()

        new_time_slice = TimeSlice.objects.create(user = request.user, begin = start_time, slip_id = slip_id )
        new_time_slice.save()
        return HttpResponse('Your timeslice begin time %s has been created' % start_time)

    elif action == 'stop':
        slice = TimeSlice.objects.get(user = request.user, slip = slip_id, end = None)

        if request.POST.has_key('end'):
            slice.end = request.POST['end']
        else:
            slice.end = datetime.now()

        slice.update_duration()
        slice.save()

        return HttpResponse('Your timeslice for slip "%s", begintime %s has been stopped at %s' % (slice.slip.name, slice.begin, slice.end))

    elif action == 'get_json':
        slip = Slip.objects.get(id = slip_id)
        if slip.is_active() == False:
            return HttpResponse("{'active' : true, 'slip_time' : '%s' }" % slip.display_time())
        else:
           return HttpResponse("{'active' : false, 'slip_time' : '%s' }" % slip.display_time())



    else:
        #Make a return for only action allowed is start/stop
        pass

@login_required()
def slip_create(request):
    if request.method != 'POST':
        return HttpResponseNotAllowed(('POST',))
    name = request.POST['name']
    new_slip = Slip.objects.create(user = request.user, name = name)
    new_slip.save()
    return HttpResponse('Your slip "%s" has been created' % name)
