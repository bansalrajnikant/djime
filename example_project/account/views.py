"""
Basic account app. 

Just here to make the example project work, since login_required
requires some sort of account handling to be present.
"""

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404

def signup(request):
   return HttpResponse('This is supposed to be the signup page, but it is not implemented in this example app.')

