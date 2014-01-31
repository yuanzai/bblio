# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Document'
        db.create_table(u'search_document', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('document_text', self.gf('django.db.models.fields.TextField')()),
            ('urlAddress', self.gf('django.db.models.fields.URLField')(max_length=1000)),
            ('domain', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.TextField')()),
            ('lastupdate', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('isUsed', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['search.Site'])),
        ))
        db.send_create_signal(u'search', ['Document'])

        # Adding model 'Site'
        db.create_table(u'search_site', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('source_allowed_domains', self.gf('django.db.models.fields.TextField')()),
            ('source_start_urls', self.gf('django.db.models.fields.TextField')()),
            ('source_allowFollow', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('source_denyFollow', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('source_allowParse', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('source_denyParse', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('lastupdate', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('parseCount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('responseCount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('grouping', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'search', ['Site'])


    def backwards(self, orm):
        # Deleting model 'Document'
        db.delete_table(u'search_document')

        # Deleting model 'Site'
        db.delete_table(u'search_site')


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
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastupdate': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'parseCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'responseCount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'source_allowFollow': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_allowParse': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_allowed_domains': ('django.db.models.fields.TextField', [], {}),
            'source_denyFollow': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_denyParse': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_start_urls': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['search']