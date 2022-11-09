# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Featured'
        db.create_table('content_featured', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('comedian', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, to=orm['content.Collection'])),
            ('show', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, to=orm['content.Collection'])),
            ('movie', self.gf('django.db.models.fields.related.OneToOneField')(related_name='+', unique=True, to=orm['content.Collection'])),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal('content', ['Featured'])


    def backwards(self, orm):
        # Deleting model 'Featured'
        db.delete_table('content_featured')


    models = {
        'content.collection': {
            'Meta': {'object_name': 'Collection'},
            'connections': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'connections_rel_+'", 'blank': 'True', 'to': "orm['content.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'role': ('django.db.models.fields.SmallIntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'blank': 'True'})
        },
        'content.featured': {
            'Meta': {'object_name': 'Featured'},
            'comedian': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['content.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'movie': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['content.Collection']"}),
            'show': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['content.Collection']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        'content.video': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Video'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': "orm['content.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['content']