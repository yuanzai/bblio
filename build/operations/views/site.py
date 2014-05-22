#python imports
import re
import urllib
import cgi
import sys

#django app imports
from build.search.models import Document, Site, TestingResult, TestingGroup, Phrase
from build.operations.forms import TestingFormPage, TestingFormResult, AdminURLListForm, SiteForm

#django imports
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, modelform_factory
from django.core.urlresolvers import reverse
from django import forms
from django.forms.models import model_to_dict

#es import
from es.YTHESController import YTHESController as ESController

#crawler import
import scraper.scrapeController
import scraper.linkextract

#distributed import
import aws.scrapeMaster
import aws.ec2

def site(request, site_id):
    if site_id !='0':
        site = Site.objects.get(pk=site_id)
    else:
        site = None

    if request.method == 'POST':
        site_form  = SiteForm(request.POST,instance=site)
        if site_form.is_valid():
            new_site = site_form.save()
            if site_id == '0':
                return HttpResponseRedirect(reverse('site', 
                    kwargs={ 'site_id' : new_site.id}))
            elif 'deny_parameters' in request.POST: 
                form_deny = request.POST['deny_parameters']
                docs = Document.objects.filter(site=site)
                site.deny_parameters=form_deny
                if form_deny[-1:] == ';':
                    form_deny = form_deny[:-1]
                denys = form_deny.split(';')
                for deny in denys:
                    d = docs.filter(urlAddress__contains=deny)
                    d.update(isUsed=1)
        else:
            return HttpResponse('Error fields: ' + str(site_form.errors))
    context = {}
    if site_id !='0':
        site = Site.objects.get(pk=site_id)
        d = (Document.objects.filter(site_id=site_id)
                .values('id','urlAddress','isUsed')
                .order_by('isUsed','urlAddress'))
        es = ESController()

        context.update({
            'doc_count' : d.count(),
            'zero_count' : Document.objects.filter(site_id=site_id).filter(isUsed=0).count(),
            'docs':d,
            'running' : site.running})

        try:
            context.update({'index_count' : es.get_document_count_for_site_id(site_id)})
        except:
            pass

        try: 
            context.update({'jobid': site.jobid,
                            'instance_ip': aws.ec2.getInstanceFromInstanceName(site.instance).ip_address})
        except:
            pass
    site_form = SiteForm(instance=site)
    context.update({
            'site_id':site_id,
            'site_form':site_form,})
    
    return render(request, 'operations/site.html',context)    

def sites(request):
    sites = Site.objects.all()
    site_list = []
    for site in sites:
        s = model_to_dict(site)
        s.update({'doc_count':Document.objects.filter(site=site).count()})
        site_list.append(s)

    context = {'sites':site_list}
    
    return render(request, 'operations/sites.html',context)
# input code
def delete(request, site_id):
    Site.objects.get(pk=site_id).delete()
    return HttpResponseRedirect(reverse('sites'))

# crawler code
def crawl(request, site_id):
    if scraper.scrapeController.get_jobs_for_site(site_id)=='Running':
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    site = Site.objects.get(pk=site_id)
    
    ret = scraper.scrapeController.curl_schedule_crawl(site_id, site.instance)
    if 'jobid' in ret:
        site.jobid = ret['jobid']
        site.save()
    else:
        return HttpResponse("Error when scheduling job")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def crawl_cancel(request, site_id):
    scraper.scrapeController.curl_cancel_crawl(site_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def clear_crawl_schedule(request, site_id):
    aws.scrapeMaster.clear_schedule(site_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#database document code
def document(request,doc_id):
    import HTMLParser
    es = ESController()
    doc = Document.objects.get(pk=doc_id)
    context = {
            'html': '<code>' + re.sub('\n','</code>\n<code>',cgi.escape(es.get_body_html(doc.document_html))) + '</code>',
            'parsed_text' : '<br>'.join(es.text_parse(doc.document_html))
            }

    return render(request, 'operations/document.html',context)


def document_reset_to_zero(request,site_id):
    Document.objects.filter(site_id=site_id).update(isUsed=0)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def document_duplicate_filter(request,site_id):
    docs = Document.objects.filter(site_id=site_id).filter(isUsed=0)
    urlList = docs.values_list('urlAddress',flat=True).distinct()
    for url in urlList:
        print(url)
        #pure duplicate
        if docs.filter(urlAddress=url).count() > 1:
            first_id = docs.filter(urlAddress=url)[0].id
            docs.filter(urlAddress=url).exclude(pk=first_id).update(isUsed=2)
            continue
        
        #https filter
        if url[:5] == 'https':
            url_http = url[:4] + url[5:]
            if docs.filter(urlAddress=url_http).count() > 0:
                docs.filter(urlAddress=url).update(isUsed=3)
                continue

        #www filter
        if url[:11] == 'https://www':
            url_www = 'https://' + url[12:]
        elif url[:10] == 'http://www':
            url_www = 'http://' + url[11:]
        else:
            url_www = None

        if url_www:
            if docs.filter(urlAddress=url_www).count() > 0:
                docs.filter(urlAddress=url_www).update(isUsed=4)
                continue

        #slash filter
        if url[-1:] == '/':
            url_slash = url[:-1]
            if docs.filter(urlAddress=url_slash).count() > 0:
                docs.filter(urlAddress=url).update(isUsed=5)
                
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def document_delete(request, site_id):
    Document.objects.filter(site_id=site_id).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#elasticsearch code
def es_index_site(request, site_id):
    es = ESController()
    es.index_site_id(site_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def es_remove_site_from_index(request, site_id):
    es = ESController()
    es.delete_site_id_from_es(site_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#others
def tree(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['url']
        level = int(request.POST['level'])
        linkno = request.POST['linkno']
        parse_parameters = None
        follow_parameters = None
        deny_parameters = None
        source_allowed_domains = None
        if request.POST['parse_parameters'] != '':
            parse_parameters = request.POST['parse_parameters']
        if request.POST['follow_parameters'] != '':
            follow_parameters = request.POST['follow_parameters']
        if request.POST['deny_parameters'] != '':
            deny_parameters = request.POST['deny_parameters']
        if request.POST['source_allowed_domains'] != '':
            source_allowed_domains = request.POST['source_allowed_domains']
        
        context = {'level' : level + 1} 
        linklist = []
        if level == 0:
            urllist = url.split(";")
            for i,eachurl in enumerate(urllist):
                linklist.append({'url':eachurl,'allow':'followed','linkno':i})
        else:
            linklist  = scraper.linkextract.link_extractor(url,parse_parameters,follow_parameters,deny_parameters,source_allowed_domains)
        context.update({'list':linklist})
    return render(request, 'operations/tree.html',context)

      
