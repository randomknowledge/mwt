# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TaskPlugin'
        db.create_table('mwt_taskplugin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dsn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=120, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(default='', max_length=120, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('versionfield', self.gf('django.db.models.fields.CharField')(default=None, max_length=12, null=True)),
            ('params', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('mwt', ['TaskPlugin'])

        # Adding model 'NotificationPlugin'
        db.create_table('mwt_notificationplugin', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dsn', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=120, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(default='', max_length=120, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('versionfield', self.gf('django.db.models.fields.CharField')(default=None, max_length=12, null=True)),
            ('params', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('mwt', ['NotificationPlugin'])

        # Adding model 'TaskPluginOption'
        db.create_table('mwt_taskpluginoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mwt.Test'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('plugin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mwt.TaskPlugin'])),
        ))
        db.send_create_signal('mwt', ['TaskPluginOption'])

        # Adding model 'NotificationPluginOption'
        db.create_table('mwt_notificationpluginoption', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mwt.Test'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('plugin', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mwt.NotificationPlugin'])),
        ))
        db.send_create_signal('mwt', ['NotificationPluginOption'])

        # Adding model 'Client'
        db.create_table('mwt_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=96)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('mwt', ['Client'])

        # Adding model 'Website'
        db.create_table('mwt_website', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=96)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mwt.Client'])),
        ))
        db.send_create_signal('mwt', ['Website'])

        # Adding model 'Test'
        db.create_table('mwt_test', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('website', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mwt.Website'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('mwt', ['Test'])

        # Adding M2M table for field tasks on 'Test'
        db.create_table('mwt_test_tasks', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('test', models.ForeignKey(orm['mwt.test'], null=False)),
            ('taskplugin', models.ForeignKey(orm['mwt.taskplugin'], null=False))
        ))
        db.create_unique('mwt_test_tasks', ['test_id', 'taskplugin_id'])

        # Adding M2M table for field notifications on 'Test'
        db.create_table('mwt_test_notifications', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('test', models.ForeignKey(orm['mwt.test'], null=False)),
            ('notificationplugin', models.ForeignKey(orm['mwt.notificationplugin'], null=False))
        ))
        db.create_unique('mwt_test_notifications', ['test_id', 'notificationplugin_id'])

        # Adding model 'Testrun'
        db.create_table('mwt_testrun', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_started', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_finished', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(default='pending', max_length=32)),
            ('result', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('task', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mwt.TaskPlugin'])),
            ('schedule', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['mwt.RunSchedule'])),
        ))
        db.send_create_signal('mwt', ['Testrun'])

        # Adding model 'RunSchedule'
        db.create_table('mwt_runschedule', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_run_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('repeat', self.gf('django.db.models.fields.CharField')(default='no', max_length=32)),
            ('test', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mwt.Test'])),
            ('paused', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('run_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_run', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal('mwt', ['RunSchedule'])


    def backwards(self, orm):
        # Deleting model 'TaskPlugin'
        db.delete_table('mwt_taskplugin')

        # Deleting model 'NotificationPlugin'
        db.delete_table('mwt_notificationplugin')

        # Deleting model 'TaskPluginOption'
        db.delete_table('mwt_taskpluginoption')

        # Deleting model 'NotificationPluginOption'
        db.delete_table('mwt_notificationpluginoption')

        # Deleting model 'Client'
        db.delete_table('mwt_client')

        # Deleting model 'Website'
        db.delete_table('mwt_website')

        # Deleting model 'Test'
        db.delete_table('mwt_test')

        # Removing M2M table for field tasks on 'Test'
        db.delete_table('mwt_test_tasks')

        # Removing M2M table for field notifications on 'Test'
        db.delete_table('mwt_test_notifications')

        # Deleting model 'Testrun'
        db.delete_table('mwt_testrun')

        # Deleting model 'RunSchedule'
        db.delete_table('mwt_runschedule')


    models = {
        'mwt.client': {
            'Meta': {'object_name': 'Client'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '96'})
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
            'schedule': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mwt.RunSchedule']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '32'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['mwt.TaskPlugin']"})
        },
        'mwt.website': {
            'Meta': {'object_name': 'Website'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mwt.Client']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '96'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['mwt']