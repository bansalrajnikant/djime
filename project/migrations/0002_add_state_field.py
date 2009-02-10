
from south.db import db
from django.db import models
from djime.models import *
import datetime
from django.utils.translation import ugettext_lazy as _

class Migration:
    
    def forwards(self):
        
        STATE_CHOICES = (
            ('active', 'Active'),
            ('on_hold', 'On Hold'),
            ('completed', 'Completed'),
            ('dropped', 'Dropped'),
        )
        db.add_column('project_project', 'state', models.CharField(max_length=31, choices=STATE_CHOICES, default='active', verbose_name=_('state')))
    
    def backwards(self):
        db.delete_column('project_project', 'state')

