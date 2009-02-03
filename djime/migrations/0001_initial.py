
from south.db import db
from django.db import models
from djime.models import *

class Migration:
    
    def forwards(self):
        
        
        # Mock Models
        User = db.mock_model(model_name='User', db_table='auth_user', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        Project = db.mock_model(model_name='Project', db_table='project_project', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        Client = db.mock_model(model_name='Client', db_table='project_client', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'Slip'
        db.create_table('djime_slip', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('name', models.CharField(max_length=128)),
            ('user', models.ForeignKey(User, related_name="slips", blank=True, null=True)),
            ('project', models.ForeignKey(Project, blank = True, null=True)),
            ('client', models.ForeignKey(Client, blank = True, null=True)),
            ('due', models.DateField(null=True, blank=True)),
            ('created', models.DateTimeField(auto_now_add=True)),
            ('updated', models.DateTimeField(auto_now=True)),
        ))
        
        # Mock Models
        Slip = db.mock_model(model_name='Slip', db_table='djime_slip', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        User = db.mock_model(model_name='User', db_table='auth_user', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'TimeSlice'
        db.create_table('djime_timeslice', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('begin', models.DateTimeField(default=datetime.datetime.now)),
            ('end', models.DateTimeField(null=True, blank=True)),
            ('slip', models.ForeignKey(Slip)),
            ('user', models.ForeignKey(User, related_name="timeslices", blank=True, null=True)),
            ('duration', models.PositiveIntegerField(editable=False, default=0)),
            ('week_number', models.PositiveIntegerField(default=datetime.datetime.now().isocalendar()[1])),
            ('create_date', models.DateField(default=datetime.datetime.now().date())),
        ))
        
        # Mock Models
        User = db.mock_model(model_name='User', db_table='auth_user', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'DataImport'
        db.create_table('djime_dataimport', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('user', models.ForeignKey(User)),
            ('created', models.DateTimeField(auto_now_add=True)),
            ('completed', models.DateTimeField(blank=True, null=True)),
            ('complete_data', models.FileField(upload_to='import_data/complete/%Y/%m/')),
            ('partial_data', models.FileField(upload_to='import_data/partial/%Y/%m/')),
        ))
        
        db.send_create_signal('djime', ['Slip','TimeSlice','DataImport'])
    
    def backwards(self):
        db.delete_table('djime_dataimport')
        db.delete_table('djime_timeslice')
        db.delete_table('djime_slip')
        
