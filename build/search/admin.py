from django.contrib import admin
from models import Site

class SiteAdmin(admin.ModelAdmin):
    list_display = ('name','grouping','parseCount',)

admin.site.register(Site,SiteAdmin)

