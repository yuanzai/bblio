from django.db import models

class Document(models.Model):
    document_text = models.TextField()
    file_name = models.CharField(max_length=200)
    urlAddress = models.URLField(max_length=500,unique='true')
    homeAddress = models.TextField()
    title = models.CharField(max_length=200)
    def __unicode__(self):
        return self.document_text

