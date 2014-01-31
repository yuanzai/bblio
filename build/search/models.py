from django.db import models

class Document(models.Model):
    document_text = models.TextField()
    urlAddress = models.URLField(max_length=1000)
    domain = models.TextField()
    title = models.TextField()
    lastupdate = models.DateTimeField(auto_now=True)
    isUsed = models.SmallIntegerField(default=1)
    site = models.ForeignKey('Site')
    def __unicode__(self):
        return self.document_text

class Site(models.Model):
    #id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)
    source_allowed_domains = models.TextField(help_text='Please separate multiple domains with ";" character. Do not end with with ";". Do not include the "http://www" or "www" at the start or any "/" at the end. For blogspot blogs, do not include the ".sg" at the end. eg. "example.com"')
    source_start_urls = models.TextField(help_text='Please separate multiple URLs with ";" character. Do not end with ";". Please use the full URL, ie include the "http://www." at the start. eg "http://www.example.com/')
    source_allowFollow = models.TextField(blank=True, null=True, help_text='Please separate search strings(terms) with ";". Do not end with ";". The code searches for an exact match. Please do not use any wild cards. Where possible, use slashes when the term is surrounded by it. ie "/post/" or "/case/". This prevents the code from picking up URLs which include the title in the URL, "this case is example".')
    source_denyFollow = models.TextField(blank=True, null=True, help_text='Please separate search strings(terms) with ";". Do not end with ";". The code searches for an exact match. Please do not use any wild cards. Where possible, use slashes when the term is surrounded by it. ie "/post/" or "/case/". This prevents the code from picking up URLs which include the title in the URL, "this case is example".')
    source_allowParse= models.TextField(blank=True, null=True, help_text='Please separate search strings(terms) with ";". Do not end with ";". The code searches for an exact match. Please do not use any wild cards. Where possible, use slashes when the term is surrounded by it. ie "/post/" or "/case/". This prevents the code from picking up URLs which include the title in the URL, "this case is example".')
    source_denyParse = models.TextField(blank=True, null=True, help_text='Please separate search strings(terms) with ";". Do not end with ";". The code searches for an exact match. Please do not use any wild cards. Where possible, use slashes when the term is surrounded by it. ie "/post/" or "/case/". This prevents the code from picking up URLs which include the title in the URL, "this case is example".')
    lastupdate = models.DateTimeField(blank=True, null=True)
    parseCount = models.IntegerField(blank=True, null=True)
    responseCount = models.IntegerField(blank=True, null=True)
    grouping = models.CharField(max_length=255, blank=True, null=True)
    running = models.BooleanField(default=False)
    depthlimit = models.IntegerField(default=0) 
