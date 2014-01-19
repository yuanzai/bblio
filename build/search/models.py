from django.db import models

class Document(models.Model):
    document_text = models.TextField()
    urlAddress = models.URLField(max_length=500)
    domain = models.TextField()
    title = models.TextField()
    lastupdate = models.DateTimeField(auto_now=True)
    isUsed = models.SmallIntegerField(default=1)
    def __unicode__(self):
        return self.document_text

class Site(models.Model):
    name = models.CharField(max_length=255,primary_key=True)
    source_allowed_domains = models.TextField()
    source_start_urls = models.TextField()
    source_allowFollow = models.TextField(blank=True, null=True) 
    source_denyFollow = models.TextField(blank=True, null=True)
    source_allowParse = models.TextField(blank=True, null=True)
    source_denyParse = models.TextField(blank=True, null=True)
    lastupdate = models.DateTimeField(blank=True, null=True)
    parseCount = models.IntegerField(blank=True, null=True)
    responseCount = models.IntegerField(blank=True, null=True)
    grouping = models.CharField(max_length=255)
