import csv
from datetime import datetime
from project.models import Project
from tracker.models import Slip, TimeSlice
from django.contrib.auth.models import User
from data_import.models import Import
import cPickle as pickle

def handle_uploaded_file(file, user_id):
    user_object = User.objects.get(pk=user_id)
    csv_reader = csv.DictReader(file, fieldnames=['date','start','end','duration','project','slip'])
    line_data = []
    for line in csv_reader:
        line_data.append(line)

    total_time = 0
    val = {}
    pickles = {'projects': [], 'slips': [], 'slices': []}
    for line in line_data[1:]:
        begin = datetime.strptime('T'.join((line['date'], line['start'])), '%Y-%m-%dT%H:%M')
        end = datetime.strptime('T'.join((line['date'], line['end'])), '%Y-%m-%dT%H:%M')
        total_time += int(line['duration'])
        if not val.has_key(line['project']):
            project_set = Project.objects.filter(name=line['project'], members = user_id)
            if  project_set:
                if len(project_set) >1:
                    project = Project()
                    project.name = line['project']
                    project_created_msg = 'Found more than one project, you are on, with same name. New project will be created.'
                    project_created_bool = True
                else:
                    project = project_set[0]
                    project_created_msg = "Found project, and will add slips and timeslices to the existing project."
                    project_created_bool = False
            else:
                project_set = Project.objects.filter(name=line['project'])
                if project_set:
                    if len(project_set) >1:
                        project = Project()
                        project.name = line['project']
                        project_created_msg = 'Found more than one project, with same name. New project will be created.'
                        project_created_bool = True
                    else:
                        project = project_set[0]
                        project_created_msg = "Found project, and will add user profile, slips and timeslices to the existing project."
                        project_created_bool = False
                else:
                    project = Project()
                    project.name = line['project']
                    project_created_msg = 'No project of that name. New project will be created'
                    project_created_bool = True
            val[line['project']] = {'created': project_created_bool, 'message': project_created_msg, 'project_object': project, 'slips': {}}
            pickles['projects'].append(project)

        if not val[line['project']]['slips'].has_key(line['slip']):
            if val[line['project']]['created']:
                slip = Slip()
                slip.name = line['slip']
                slip.user = user_object
                slip.project = val[line['project']]['project_object']
                slip.created = line['date']
                slip_created_bool = True

            else:
                slip_set = Slip.objects.filter(name = line['slip'], user = user_object , project = project)
                if not slip_set or len(slip_set) > 1:
                    slip = Slip()
                    slip.name = line['slip']
                    slip.user = user_object
                    slip.project = val[line['project']]['project_object']
                    slip.created = line['date']
                    slip_created_bool = True
                else:
                    slip = slip_set[0]
                    slip_created_bool = False
            val[line['project']]['slips'][line['slip']]={'created': slip_created_bool, 'slip_object': slip, 'slices': []}
            pickles['slips'].append(slip)

        if val[line['project']]['slips'][line['slip']]['created']:
            slice = TimeSlice()
            slice.begin = begin
            slice.end = end
            slice.duration = int(line['duration'])
            slice.slip = val[line['project']]['slips'][line['slip']]['slip_object']
            slice.user = user_object
            slice_created_bool = True
        else:
            slice_set = TimeSlice.objects.filter(begin = begin, end = end, duration = int(line['duration']), slip = slip, user = user_object)
            if slice_set:
                if len(slice_set) > 1:
                    pass
                slice = slice_set[0]
                slice_created_bool = False
            else:
                slice = TimeSlice()
                slice.begin = begin
                slice.end = end
                slice.duration = int(line['duration'])
                slice.slip = val[line['project']]['slips'][line['slip']]['slip_object']
                slice.user = user_object
                slice_created_bool = True
        val[line['project']]['slips'][line['slip']]['slices'].append(slice)
        pickles['slices'].append(slice)

    total_time = str(int(total_time/3600.0))+'h'

    import_data = Import()
    import_data.complete_data = pickle.dumps(pickles)
    import_data.partial_data = pickle.dumps({'import_data': line_data[1:11]})
    import_data.user = user_object
    import_data.save()

    return pickling.id

def importer_preview(import_id):
    pickle = Import.objects.get(pk=import_id)
    dict = pickle.loads(str(pickle.partial_data))
    return dict

def importer_save(import_id, user_id):
    if user_id != Import.objects.get(pk=import_id).user_id:
        return 'Invalid user'
    import_data = Import.objects.get(pk=import_id)
    dict = pickle.loads(str(pickle.complete_data))
    for project in dict['projects']:
        project.save()
    for slip in dict['slips']:
        slip.project = slip.project
        slip.save()
    for slice in dict['slices']:
        slice.slip = slice.slip
        slice.update_date()
    import_data.delete()
    return 'succes'

def importer_delete(import_id, user_id):
    if user_id != Import.objects.get(pk=import_id).user_id:
        return 'Invalid user'
    Import.objects.get(pk=import_id).delete()
    return 'succes'
