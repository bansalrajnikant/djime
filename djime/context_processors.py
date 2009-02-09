"""
Django context processors used within Djime.
"""
from django.conf import settings

def static_urls(request):
    return {'STATIC_URL': settings.STATIC_URL,
            'DEMO_STATIC_URL': settings.EXTERNAL_STATIC_URL}

