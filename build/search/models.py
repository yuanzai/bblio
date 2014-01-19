from django.db import models

class Document(models.Model):
    document_text = models.TextField()
    urlAddress = models.URLField(max_length=500)
    domain = models.TextField()
    title = models.TextField()
    lastupdate = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.document_text

class Site(models.Model):
    name = models.CharField(max_length=255,primary_key=True)
    source_allowed_domains = models.TextField()
    source_start_urls = models.TextField()
    source_allowFollow = models.TextField() 
    source_denyFollow = models.TextField()
    source_allowParse = models.TextField() 
    source_denyParse = models.TextField()
    lastupdate = models.DateField()
    parseCount = models.IntegerField()
    grouping = models.CharField(max_length=255)
