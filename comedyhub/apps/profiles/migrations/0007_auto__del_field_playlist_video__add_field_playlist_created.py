# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Playlist.video'
        db.delete_column('profiles_playlist', 'video_id')

        # Adding field 'Playlist.created'
        db.add_column('profiles_playlist', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding M2M table for field videos on 'Playlist'
        db.create_table('profiles_playlist_videos', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('playlist', models.ForeignKey(orm['profiles.playlist'], null=False)),
            ('video', models.ForeignKey(orm['content.video'], null=False))
        ))
        db.create_unique('profiles_playlist_videos', ['playlist_id', 'video_id'])


    def backwards(self, orm):
        # Adding field 'Playlist.video'
        db.add_column('profiles_playlist', 'video',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['content.Video']),
                      keep_default=False)

        # Deleting field 'Playlist.created'
        db.delete_column('profiles_playlist', 'created')

        # Removing M2M table for field videos on 'Playlist'
        db.delete_table('profiles_playlist_videos')


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
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'profiles.feeling': {
            'Meta': {'object_name': 'Feeling'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['profiles.Profile']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.utcnow'}),
            'video': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['content.Video']"})
        },
        'profiles.playlist': {
            'Meta': {'object_name': 'Playlist'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'playlists'", 'to': "orm['profiles.Profile']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'videos': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'playlists'", 'null': 'True', 'to': "orm['content.Video']"})
        },
        'profiles.profile': {
            'Meta': {'object_name': 'Profile'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'feelings': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'feelers'", 'null': 'True', 'through': "orm['profiles.Feeling']", 'to': "orm['content.Video']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['profiles']