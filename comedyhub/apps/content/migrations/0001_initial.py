# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Collection'
        db.create_table('content_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('role', self.gf('django.db.models.fields.SmallIntegerField')()),
        ))
        db.send_create_signal('content', ['Collection'])

        # Adding M2M table for field connections on 'Collection'
        db.create_table('content_collection_connections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_collection', models.ForeignKey(orm['content.collection'], null=False)),
            ('to_collection', models.ForeignKey(orm['content.collection'], null=False))
        ))
        db.create_unique('content_collection_connections', ['from_collection_id', 'to_collection_id'])

        # Adding model 'Video'
        db.create_table('content_video', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='videos', to=orm['content.Collection'])),
        ))
        db.send_create_signal('content', ['Video'])


    def backwards(self, orm):
        # Deleting model 'Collection'
        db.delete_table('content_collection')

        # Removing M2M table for field connections on 'Collection'
        db.delete_table('content_collection_connections')

        # Deleting model 'Video'
        db.delete_table('content_video')


    models = {
        'content.collection': {
            'Meta': {'object_name': 'Collection'},
            'connections': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'connections_rel_+'", 'to': "orm['content.Collection']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'role': ('django.db.models.fields.SmallIntegerField', [], {})
        },
        'content.video': {
            'Meta': {'object_name': 'Video'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': "orm['content.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['content']