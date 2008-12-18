from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from data_import.forms import DataImportForm
from data_import.importer import handle_uploaded_file

@login_required
def import_form(request):
    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['import_file'])
            return HttpResponseRedirect(reverse('data_import_confirm'))
    else:
        form = DataImportForm()
    return render_to_response('data_import/upload.html', {'form': form},
                              context_instance=RequestContext(request))

def confirm(request):
    return render_to_response('data_import/confirm.html', {},
                              context_instance=RequestContext(request))

def results(request):
    return render_to_response('data_import/results.html', {},
                              context_instance=RequestContext(request))