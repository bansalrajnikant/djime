from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
    return HttpResponseNotAllowed()

def slip(request, slip_id):
    return HttpResponseNotAllowed(('GET', 'PUT', 'DELETE'))

def slip_action(request, slip_id, action):
    return HttpResponseNotAllowed(('PUT',))

def slip_create(request):
    return HttpResponseNotAllowed(('POST',))
