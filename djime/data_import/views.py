import cPickle as pickle
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from djime.data_import.forms import DataImportForm
from djime.models import DataImport
from djime.data_import.importer import handle_uploaded_file, importer_save


@login_required
def import_form(request):
    if request.method == 'POST':
        form = DataImportForm(request.POST, request.FILES)
        if form.is_valid():
            import_id = handle_uploaded_file(request.FILES['import_file'], request.user.id)
            action = 'confirm'
            return HttpResponseRedirect(reverse('data_import_action', args=(import_id, action)))
    else:
        form = DataImportForm()
    return render_to_response('data_import/upload.html', {'form': form},
                              context_instance=RequestContext(request))
@login_required
def action(request, import_id, action):
    import_data = get_object_or_404(DataImport, pk=import_id, completed=None)
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
            importer_save(import_data, request.user)
            request.user.message_set.create(message='Import successful.')
        elif action == 'cancel':
            import_data.delete()
            request.user.message_set.create(message='Import cancelled.')
        else:
            return HttpResponseForbidden('Invalid post action')

        return HttpResponseRedirect(reverse('djime_index'))

