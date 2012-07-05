# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MWTGroup'
        db.create_table('mwt_mwtgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=96)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mwt', ['MWTGroup'])

        # Adding M2M table for field users on 'MWTGroup'
        db.create_table('mwt_mwtgroup_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mwtgroup', models.ForeignKey(orm['mwt.mwtgroup'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('mwt_mwtgroup_users', ['mwtgroup_id', 'user_id'])

        # Adding M2M table for field users on 'Website'
        db.create_table('mwt_website_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('website', models.ForeignKey(orm['mwt.website'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('mwt_website_users', ['website_id', 'user_id'])

        # Adding M2M table for field groups on 'Website'
        db.create_table('mwt_website_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('website', models.ForeignKey(orm['mwt.website'], null=False)),
            ('mwtgroup', models.ForeignKey(orm['mwt.mwtgroup'], null=False))
        ))
        db.create_unique('mwt_website_groups', ['website_id', 'mwtgroup_id'])

        # Adding M2M table for field users on 'Client'
        db.create_table('mwt_client_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm['mwt.client'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('mwt_client_users', ['client_id', 'user_id'])

        # Adding M2M table for field groups on 'Client'
        db.create_table('mwt_client_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('client', models.ForeignKey(orm['mwt.client'], null=False)),
            ('mwtgroup', models.ForeignKey(orm['mwt.mwtgroup'], null=False))
        ))
        db.create_unique('mwt_client_groups', ['client_id', 'mwtgroup_id'])


    def backwards(self, orm):
        # Deleting model 'MWTGroup'
        db.delete_table('mwt_mwtgroup')

        # Removing M2M table for field users on 'MWTGroup'
        db.delete_table('mwt_mwtgroup_users')

        # Removing M2M table for field users on 'Website'
        db.delete_table('mwt_website_users')

        # Removing M2M table for field groups on 'Website'
        db.delete_table('mwt_website_groups')

        # Removing M2M table for field users on 'Client'
        db.delete_table('mwt_client_users')

        # Removing M2M table for field groups on 'Client'
        db.delete_table('mwt_client_groups')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'mwt.client': {
            'Meta': {'object_name': 'Client'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mwt.MWTGroup']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '96'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'mwt.mwtgroup': {
            'Meta': {'object_name': 'MWTGroup'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '96'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'mwt.notificationplugin': {
            'Meta': {'object_name': 'NotificationPlugin'},
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '120', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dsn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '120', 'blank': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'versionfield': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'null': 'True'})
        },
        'mwt.notificationpluginoption': {
            'Meta': {'object_name': 'NotificationPluginOption'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mwt.NotificationPlugin']"}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mwt.Test']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mwt.runschedule': {
            'Meta': {'object_name': 'RunSchedule'},
            'first_run_at': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_run': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paused': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'repeat': ('django.db.models.fields.CharField', [], {'default': "'no'", 'max_length': '32'}),
            'run_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mwt.Test']"})
        },
        'mwt.taskplugin': {
            'Meta': {'object_name': 'TaskPlugin'},
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '120', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dsn': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '120', 'blank': 'True'}),
            'params': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'versionfield': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '12', 'null': 'True'})
        },
        'mwt.taskpluginoption': {
            'Meta': {'object_name': 'TaskPluginOption'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'plugin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mwt.TaskPlugin']"}),
            'test': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mwt.Test']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'mwt.test': {
            'Meta': {'object_name': 'Test'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notifications': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['mwt.NotificationPlugin']"}),
            'tasks': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': "orm['mwt.TaskPlugin']"}),
            'website': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mwt.Website']"})
        },
        'mwt.testrun': {
            'Meta': {'object_name': 'Testrun'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_finished': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_started': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'result': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'result_successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mwt.RunSchedule']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '32'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mwt.TaskPlugin']"})
        },
        'mwt.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'profile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'mwt.website': {
            'Meta': {'object_name': 'Website'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mwt.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['mwt.MWTGroup']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        }
    }

    complete_apps = ['mwt']