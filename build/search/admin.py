from django.contrib import admin
from models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from models import Document
import views

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name','id','grouping','depthlimit','show_current_doc_count','parseCount','responseCount','lastupdate','show_urls_parsed','delete_doc',)
    # fields = ('name','grouping','source_allowed_domains','source_start_urls','source_allowParse','source_denyParse','source_allowFollow','source_denyFollow')
    list_editable = ('grouping','depthlimit')
    ordering = ('grouping',)
    exclude = ('id','lastupdate','parseCount','responseCount')
    readonly_fields = ('id',)

    def show_current_doc_count(self, obj):
        return Document.objects.filter(site=obj).count()
    show_current_doc_count.short_description = 'Doc Count'

    def show_urls_parsed(self, obj):
        return '<a href="%s">%s</a>' % (reverse('search:scraped', args=(str(obj.id),)), 'URL List')
    show_urls_parsed.allow_tags = True
    show_urls_parsed.short_description = 'Parsed URLs'

    def delete_doc(self, obj):
        return '<a href="%s">%s</a>' % (reverse('search:delete', args=(str(obj.id),)), 'Delete docs')
    delete_doc.allow_tags = True
admin.site.register(Site,SiteAdmin)

