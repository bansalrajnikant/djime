
from south.db import db
from django.db import models
from teams.models import *

class Migration:
    
    def forwards(self):
        
        
        # Mock Models
        User = db.mock_model(model_name='User', db_table='auth_user', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # Model 'Team'
        db.create_table('teams_team', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('slug', models.SlugField(_('slug'), unique=True)),
            ('name', models.CharField(_('name'), max_length=80, unique=True)),
            ('creator', models.ForeignKey(User, related_name="created_groups", verbose_name=_('creator'))),
            ('created', models.DateTimeField(_('created'), default=datetime.now)),
            ('description', models.TextField(_('description'))),
            ('deleted', models.BooleanField(_('deleted'), default=False)),
        ))
        # Mock Models
        Team = db.mock_model(model_name='Team', db_table='teams_team', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        User = db.mock_model(model_name='User', db_table='auth_user', db_tablespace='', pk_field_name='id', pk_field_type=models.AutoField, pk_field_args=[], pk_field_kwargs={})
        
        # M2M field 'Team.members'
        db.create_table('teams_team_members', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('team', models.ForeignKey(Team, null=False)),
            ('user', models.ForeignKey(User, null=False))
        )) 
        
        db.send_create_signal('teams', ['Team'])
    
    def backwards(self):
        db.delete_table('teams_team_members')
        db.delete_table('teams_team')
        
