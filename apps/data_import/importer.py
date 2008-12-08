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

    reference = line_data[0]
    data_preview = 'Reference (Not to be included):'
    i = 0
    while i < 12:
        data_preview += 'Date: ' + str(value_list[i]['date']) + ', Start: ' + str(value_list[i]['start']) + ', End: ' + str(value_list[i]['end']) + ', Duration: ' + str(value_list[i]['duration']) + ', Project: ' + str(value_list[i]['project']) + ', Slip: ' + str(value_list[i]['slip']) + '<br>'
        i += 1

    total_time = 0
    val = {}
    pickles = {'projects': [], 'slips': [], 'slices': []}
    for dicts in line_data[1:]:
        date_list = dicts['date'].split('-')
        begin_list = dicts['start'].split(':')
        end_list = dicts['end'].split(':')
        begin = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(begin_list[0]), int(begin_list[1]))
        end = datetime(int(date_list[0]), int(date_list[1]), int(date_list[2]), int(end_list[0]), int(end_list[1]))
        total_time += int(dicts['duration'])
        if not val.has_key(dicts['project']):
            project_set = Project.objects.filter(name=dicts['project'], members = user_id)
            if  project_set:
                if len(project_set) >1:
                    project = Project()
                    project.name = dicts['project']
                    project_created_msg = 'Found more than one project, you are on, with same name. New project will be created.'
                    project_created_bool = True
                else:
                    project = project_set[0]
                    project_created_msg = "Found project, and will add slips and timeslices to the existing project."
                    project_created_bool = False
            else:
                project_set = Project.objects.filter(name=dicts['project'])
                if project_set:
                    if len(project_set) >1:
                        project = Project()
                        project.name = dicts['project']
                        project_created_msg = 'Found more than one project, with same name. New project will be created.'
                        project_created_bool = True
                    else:
                        project = project_set[0]
                        project_created_msg = "Found project, and will add user profile, slips and timeslices to the existing project."
                        project_created_bool = False
                else:
                    project = Project()
                    project.name = dicts['project']
                    project_created_msg = 'No project of that name. New project will be created'
                    project_created_bool = True
            val[dicts['project']] = {'created': project_created_bool, 'message': project_created_msg, 'project_object': project, 'slips': {}}
            pickles['projects'].append(project)

        if not val[dicts['project']]['slips'].has_key(dicts['slip']):
            if val[dicts['project']]['created']:
                slip = Slip()
                slip.name = dicts['slip']
                slip.user = user_object
                slip.project = val[dicts['project']]['project_object']
                slip.created = dicts['date']
                slip_created_bool = True

            else:
                slip_set = Slip.objects.filter(name = dicts['slip'], user = user_object , project = project)
                if not slip_set or len(slip_set) > 1:
                    slip = Slip()
                    slip.name = dicts['slip']
                    slip.user = user_object
                    slip.project = val[dicts['project']]['project_object']
                    slip.created = dicts['date']
                    slip_created_bool = True
                else:
                    slip = slip_set[0]
                    slip_created_bool = False
            val[dicts['project']]['slips'][dicts['slip']]={'created': slip_created_bool, 'slip_object': slip, 'slices': []}
            pickles['slips'].append(slip)

        if val[dicts['project']]['slips'][dicts['slip']]['created']:
            slice = TimeSlice()
            slice.begin = begin
            slice.end = end
            slice.duration = int(dicts['duration'])
            slice.slip = val[dicts['project']]['slips'][dicts['slip']]['slip_object']
            slice.user = user_object
            slice_created_bool = True
        else:
            slice_set = TimeSlice.objects.filter(begin = begin, end = end, duration = int(dicts['duration']), slip = slip, user = user_object)
            if slice_set:
                if len(slice_set) >1:
                    #send email to admin about double slices error.
                    # send_mail('Double timeslices', 'User %s has two timeslices in slip id %s', % (user_id, slip.id) 'admin@hosted.com', ['admin@hosted.com'], fail_silently=False)
                    pass
                slice = slice_set[0]
                slice_created_bool = False
            else:
                slice = TimeSlice()
                slice.begin = begin
                slice.end = end
                slice.duration = int(dicts['duration'])
                slice.slip = val[dicts['project']]['slips'][dicts['slip']]['slip_object']
                slice.user = user_object
                slice_created_bool = True
        val[dicts['project']]['slips'][dicts['slip']]['slices'].append(slice)
        pickles['slices'].append(slice)

    total_time = str(int(total_time/3600.0))+'h'

    data_preview += 'Total Time: %s <br>Number of projects: %s <br>Number of Slips: %s <br>Number of TimeSlices: %s <br>' % (total_time, len(val.keys()), len(pickles['slips']),len(pickles['slices']))
    import_data = Import()
    import_data.complete_data = pickle.dumps(pickles)
    import_data.partial_data = pickle.dumps({'import_data': line_data[1:11], 'preview': data_preview})
    import_data.user = user_object
    import_data.save()

    return pickling.id

def depickle_preview(import_id):
    pickle = Import.objects.get(pk=import_id)
    dict = pickle.loads(str(pickle.partial_data))
    return dict

def depickle_import(import_id, user_id):
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

def delete_pickles(import_id, user_id):
    if user_id != Import.objects.get(pk=import_id).user_id:
        return 'Invalid user'
    Import.objects.get(pk=import_id).delete()
    return 'succes'
