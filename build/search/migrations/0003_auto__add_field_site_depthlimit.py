# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Site.depthlimit'
        db.add_column(u'search_site', 'depthlimit',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Site.depthlimit'
        db.delete_column(u'search_site', 'depthlimit')


    models = {
        u'search.document': {
            'Meta': {'object_name': 'Document'},
            'document_text': ('django.db.models.fields.TextField', [], {}),
            'domain': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isUsed': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'lastupdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Site']"}),
            'title': ('django.db.models.fields.TextField', [], {}),
            'urlAddress': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        },
        u'search.site': {
            'Meta': {'object_name': 'Site'},
            'depthlimit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastupdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'parseCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'responseCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'running': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_allowFollow': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_allowParse': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_allowed_domains': ('django.db.models.fields.TextField', [], {}),
            'source_denyFollow': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_denyParse': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_start_urls': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['search']