# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Site.owner'
        db.add_column(u'search_site', 'owner',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Site.owner'
        db.delete_column(u'search_site', 'owner')


    models = {
        u'search.document': {
            'Meta': {'object_name': 'Document'},
            'document_html': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'document_text': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.TextField', [], {}),
            'encoding': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isUsed': ('django.db.models.fields.SmallIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'lastupdate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'publish_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'response_code': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Site']"}),
            'title': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'update_group': ('django.db.models.fields.SmallIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'urlAddress': ('django.db.models.fields.URLField', [], {'max_length': '1000'})
        },
        u'search.job': {
            'Meta': {'object_name': 'Job'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'scrapyd_job_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Site']"})
        },
        u'search.phrase': {
            'Meta': {'object_name': 'Phrase'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phrase': ('django.db.models.fields.TextField', [], {})
        },
        u'search.site': {
            'Meta': {'object_name': 'Site'},
            'deny_parameters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'depthlimit': ('django.db.models.fields.IntegerField', [], {'default': '30'}),
            'follow_parameters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'jobid': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'jurisdiction': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'lastupdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'parseCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'parse_parameters': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'responseCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'running': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_allowFollow': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_allowParse': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_allowed_domains': ('django.db.models.fields.TextField', [], {}),
            'source_denyFollow': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_denyParse': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_start_urls': ('django.db.models.fields.TextField', [], {})
        },
        u'search.testinggroup': {
            'Meta': {'object_name': 'TestingGroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'search.testingresult': {
            'Meta': {'object_name': 'TestingResult'},
            'document': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.Document']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'searchterm': ('django.db.models.fields.TextField', [], {}),
            'testinggroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['search.TestingGroup']"})
        }
    }

    complete_apps = ['search']