from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.html import escape
from django.utils.translation import ugettext as trans
from djime.forms import SlipAddForm, SlipChangeForm
from djime.models import Slip, TimeSlice
from project.models import Client, Project
try:
    import json
except ImportError:
    from django.utils import simplejson as json


@login_required()
def dashboard(request):
    display_data = {
        'slip_list': Slip.objects.filter(user=request.user).order_by('-updated')[:10],
        'project_list': Project.objects.filter(members=request.user.id, state='active')[:10],
        'slip_add_form': SlipAddForm()
    }
    return render_to_response('djime/index.html', display_data,
                              context_instance=RequestContext(request))


@login_required
def index(request):
    return render_to_response('djime/slip_index.html',
                              {'slip_list': Slip.objects.filter(user=request.user),
                               'slip_add_form': SlipAddForm()
                               },
                              context_instance=RequestContext(request))

@login_required()
def slip(request, slip_id):
    valid_methods = ('GET', 'POST', 'DELETE')

    if request.method not in valid_methods:
        return HttpResponseNotAllowed(('GET', 'POST', 'DELETE'))
    else:
        slip = get_object_or_404(Slip, pk=slip_id)
        if request.user != slip.user:
            return HttpResponseForbidden(trans('Access denied'))

        if request.method == 'GET':
            return render_to_response('djime/slip.html',
                                        {'slip': slip,
                                        'slip_change_form': SlipChangeForm()
                                        },
                                        context_instance=RequestContext(request))

        elif request.method == 'DELETE':
            slip.delete()
            # TODO: Send a message to the user that deltion succeeded.
            return HttpResponse('Successfully deleted slip %s' % slip.name)

        elif request.method == 'POST':
            slip = Slip.objects.get(id = slip_id)
            if request.POST.has_key('name'):
                old_name = slip.name
                slip.name = request.POST['name']
                slip.save()
                return HttpResponse("%s" % slip.name)
            else:
                post_data = request.POST.copy()
                # Inject the user into the post data, so we can validate based
                # on the user.
                post_data['user'] = request.user
                form = SlipChangeForm(post_data, instance=slip)
                if form.is_valid():
                    form.save()
                    # After saving the form, reinitiate the form to clear the data on return.
                    form = SlipChangeForm()
                return render_to_response('djime/slip.html',
                                                        {'slip_id': slip_id,
                                                        'slip': slip,
                                                        'slip_change_form': form,
                                                        },
                                                        context_instance=RequestContext(request))


@login_required()
def slip_action(request, slip_id, action):
    if request.method not in ('GET', 'POST'):
        return HttpResponseNotAllowed(('POST', 'GET'))

    if action == 'start':
        # Make sure the user doesn't already have an active time slice
        # for this Slip
        if not TimeSlice.objects.filter(user=request.user,
                                        slip=slip_id, end=None):
            if request.POST.has_key('begin'):
                start_time = request.POST['begin']
            else:
                start_time = datetime.now()

            # Stop active timeslices if any
            slice_query_set = TimeSlice.objects.filter(user=request.user, end=None)
            if slice_query_set:
                for slice in slice_query_set:
                    slice.end = datetime.now()
                    slice.save() # updates duration and saves the timeslice using signals.py

            new_time_slice = TimeSlice.objects.create(user = request.user, begin = start_time, slip_id = slip_id )
            new_time_slice.save()
            return HttpResponse(trans('Your timeslice begin time %(start_time)s has been created') % {'start_time': start_time})
        else:
            return HttpResponse(trans('You already have an unfinished time slice for this task. A new one has not been created.'), status=409)

    elif action == 'stop':
        slice = TimeSlice.objects.get(user = request.user, slip = slip_id, end = None)

        if request.POST.has_key('end'):
            slice.end = request.POST['end']
        else:
            slice.end = datetime.now()
        # Saving the TimeSlice model also updates the duration. This is done
        # through the pre_save signal and the timeslice_save function in signals.py
        slice.save()
        return HttpResponse(trans('Your timeslice for slip "%(name)s", begintime %(begin)s has been stopped at %(end)s') % {'name': slice.slip.name, 'begin': slice.begin, 'end': slice.end})

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
    if request.method not in ('GET', 'POST'):
        return HttpResponseNotAllowed(('POST', 'GET'))

    if request.method == 'POST':
        post_data = request.POST.copy()
        # Inject the user into the post data, so we can validate based
        # on the user.
        post_data['user'] = request.user

        form = SlipAddForm(post_data)
        if form.is_valid():
            new_slip = form.save(commit=False)
            new_slip.user = request.user
            new_slip.save()
            return HttpResponse("slip/%s" % new_slip.pk)
            # the below code was used before jQuery dialog form.js was introduced.
            # return HttpResponseRedirect(reverse('slip_page',
            #                                        kwargs={'slip_id': new_slip.id}))

        else:
            return render_to_response('djime/slip_create.html',
                                        {'slip_add_form': form,
                                        },
                                        context_instance=RequestContext(request))

    if request.method == 'GET':
        slip_add_form = SlipAddForm()
        return render_to_response('djime/slip_create.html',
                                  {'slip_add_form': SlipAddForm(),
                                  },
                                  context_instance=RequestContext(request))

