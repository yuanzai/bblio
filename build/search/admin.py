from django.contrib import admin
from models import Site

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name','grouping',)

admin.site.register(Site,SiteAdmin)

