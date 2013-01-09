# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
        for video in orm.Video.objects.all():
            video.duration = self._convert_to_time_repr(video.duration)
            video.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        for video in orm.Video.objects.all():
            video.duration = self._convert_to_seconds_repr(video.duration)
            video.save()

    def _convert_to_time_repr(self, val):
        str_val = '0%s' % datetime.timedelta(seconds=int(val))
        bits = str_val.split(':')
        # If there is no hour, we don't keep it in the final repr
        if bits[0].count('0') == 2:
            return ':'.join(bits[1:])
        return ':'.join(bits)

    def _convert_to_seconds_repr(self, val):
        bits = val.split(':')
        sec_val = 0
        # We split the bits, multiply by 60 if they're not seconds
        # and add them together.
        for i, bit in enumerate(bits):
            sec_val += int(bit)
            if i < len(bits) - 1:
                sec_val *= 60
        return sec_val

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
        'content.video': {
            'Meta': {'object_name': 'Video'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': "orm['content.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['content']
    symmetrical = True
