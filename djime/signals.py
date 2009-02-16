import datetime
def timeslice_save(sender, **kwargs):
    time_slice = kwargs['instance']
    time_slice.week_number = time_slice.begin.isocalendar()[1]
    time_slice.slip.updated = datetime.datetime.now()
    time_slice.user = time_slice.slip.user
    time_slice.slip.save()    
    if time_slice.end:
        time = time_slice.end - time_slice.begin
        time_slice.duration = time.days * 86400 + time.seconds
    else:
        time_slice.duration = 0