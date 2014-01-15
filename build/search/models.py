from django.db import models

class Document(models.Model):
    document_text = models.TextField()
    urlAddress = models.URLField(max_length=500,unique='true')
    domain = models.TextField()
    title = models.TextField()
    def __unicode__(self):
        return self.document_text

