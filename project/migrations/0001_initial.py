
from south.db import db
from django.db import models
from project.models import *

class Migration:
    
    def forwards(self):
        
        # Model 'Client'
        db.create_table('project_client', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('name', models.CharField(max_length=128, verbose_name=_('name'))),
        ))
        
        # Mock Models
        Team = db.mock_model(model_name='Team', db_table='teams_team', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        Client = db.mock_model(model_name='Client', db_table='project_client', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'Project'
        db.create_table('project_project', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('name', models.CharField(max_length=128, verbose_name=_('name'))),
            ('team', models.ForeignKey(Team, null=True, blank = True, verbose_name=_('team'))),
            ('client', models.ForeignKey(Client, null=True, blank=True, verbose_name=_('client'))),
            ('deadline', models.DateField(null=True, blank=True, verbose_name=_('deadline'))),
        ))
        # Mock Models
        Project = db.mock_model(model_name='Project', db_table='project_project', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        User = db.mock_model(model_name='User', db_table='auth_user', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # M2M field 'Project.members'
        db.create_table('project_project_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(Project, null=False)),
            ('user', models.ForeignKey(User, null=False))
        )) 
        
        db.send_create_signal('project', ['Client','Project'])
    
    def backwards(self):
        db.delete_table('project_project_members')
        db.delete_table('project_project')
        db.delete_table('project_client')
        
