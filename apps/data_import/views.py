from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from data_import.forms import DataImportForm
from data_import.models import Import
from data_import.importer import handle_uploaded_file, importer_preview, importer_save, importer_delete
import cPickle as pickle


@login_required
def import_form(request):
    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            import_id = handle_uploaded_file(request.FILES['import_file'], request.user.id)
            action = 'confirm'
            return HttpResponseRedirect(reverse('data_import_confirm', args=(import_id, action)))
    else:
        form = DataImportForm()
    return render_to_response('data_import/upload.html', {'form': form},
                              context_instance=RequestContext(request))
@login_required
def confirm(request, import_id, action):
    import_data = get_object_or_404(Import, pk=import_id, completed=None)
    if request.user.id != import_data.user_id:
        return HttpResponseForbidden('Access denied')

    if request.method == 'GET':
        if action == 'confirm':
            preview_data = pickle.loads(import_data.partial_data.read())
            return render_to_response('data_import/confirm.html',
                                      {'import_data': preview_data, 'import_id': import_id},
                                      context_instance=RequestContext(request))

    if request.method == 'POST':
        if action == 'save':
            result = importer_save(import_id, request.user.id)
            message = 'Your data have not been saved'
        elif action == 'cancel':
            result = importer_delete(import_id, request.user.id)
            message = 'Your data have not been saved'
        else:
            return HttpResponseForbidden('Invalid post action')

        if result == 'succes':
            return render_to_response('data_import/results.html',
                                      {'result': message},
                                      context_instance=RequestContext(request))
        else:
            return HttpResponse(result)
