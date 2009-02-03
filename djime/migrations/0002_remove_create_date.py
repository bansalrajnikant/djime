
from south.db import db
from django.db import models
from djime.models import *
import datetime

class Migration:
    
    def forwards(self):
        db.delete_column('djime_timeslice', 'create_date')
    
    def backwards(self):
        db.add_column('djime_timeslice', 'create_date',
                      models.DateField(default=datetime.date.today())),

