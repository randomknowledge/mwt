# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Testrun.result_successful'
        db.add_column('mwt_testrun', 'result_successful',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Testrun.result_successful'
        db.delete_column('mwt_testrun', 'result_successful')


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
            'result_successful': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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