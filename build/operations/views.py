#python imports
import re
import urllib
import cgi
import sys

#django app imports
from search.models import Document, Site, TestingResult, TestingGroup, Phrase
from forms import TestingFormPage, TestingFormResult, AdminURLListForm, SiteForm

#django imports
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory, modelform_factory
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django import forms

#es import
import es
import index1 as indexer

#crawler import
sys.path.append('/home/ec2-user/bblio/scraper/')
import scrapeController
import linkextract

def index(request):
    context = { 'es_count' : es.show('legal-index')['count']}
    return render(request,'operations/index.html',context)

def tree(request):
    context = {}
    if request.method == 'POST':
        url = request.POST['url']
        print url
        level = int(request.POST['level'])
        linkno = request.POST['linkno']
        allowF = None
        allowP = None
        denyF = None
        denyP = None
        
        if request.POST['allowF'] != '':
            allowF = request.POST['allowF'].split(";")
        if request.POST['allowP'] != '':
            allowP = request.POST['allowP'].split(";")
        if request.POST['denyF'] != '':
            denyF = request.POST['denyF'].split(";")
        if request.POST['denyP'] != '':
            denyP = request.POST['denyP'].split(";")
        context = {'level' : level + 1} 
        linklist = []
        if level == 0:
            urllist = url.split(";")
            for i,eachurl in enumerate(urllist):
                linklist.append({'url':eachurl,'allow':'followed','linkno':i})
        else:
            linklist  = linkextract.link_extractor(url,allowP,denyP,allowF,denyF)
        context.update({'list':linklist})
    return render(request, 'operations/tree.html',context)

def crawl(request, site_id):
    
    call_command('crawl',site_id)
    
    return HttpResponse('Running %s' % str(site_id))


def phrases(request):
    PhraseForm = modelform_factory(Phrase)
    
    if request.method == 'POST':
        """
        form = PhraseForm(request.POST)
        form.save()
        """
        phrases = request.POST['phrase'].encode('ascii','ignore').split('\r\n')
        for p in phrases:
            if p:
                p = p.decode('utf-8')
                p = p.strip()
                p = p.replace('-',' ')
                p = p.lower()
                if ' ' in p:
                    if Phrase.objects.filter(phrase=p).count() == 0:
                        print('save: ' + p)
                        newphrase = Phrase()
                        newphrase.phrase = p
                        newphrase.save()

    form = modelform_factory(Phrase,
            widgets={ 'phrase' : forms.Textarea(attrs={'class': 'form-control'})})
    
    phrases = Phrase.objects.all()

    context = { 'phrases' : phrases, 'form' : form }
    return render(request, 'operations/phrases.html',context)

def site(request, site_id):
    if site_id !='0':
        site = Site.objects.get(pk=site_id)
    else:
        site = None

    if request.method == 'POST':
        site_form  = SiteForm(request.POST,instance=site)
        if site_form.is_valid():
            site_form.save()
        form_deny = request.POST['source_denyParse']
        docs = Document.objects.filter(site=site)
        site.source_denyParse=form_deny
        if form_deny[-1:] == ';':
            form_deny = form_deny[:-1]
        denys = form_deny.split(';')
        for deny in denys:
            d = docs.filter(urlAddress__contains=deny)
            d.update(isUsed=1)
    context = {}
    if site_id !='0':
        site = Site.objects.get(pk=site_id)
        d = (Document.objects.filter(site_id=site_id)
                .values('id','urlAddress','isUsed')
                .order_by('isUsed','urlAddress'))
        context.update({'doc_count':d.count()})
        context.update({'zero_count':Document.objects.filter(site_id=site_id).filter(isUsed=0).count()})
                
        context.update({'docs':d})

    site_form = SiteForm(instance=site)
    context.update({
            'site_id':site_id,
            'site_form':site_form,})
    

    return render(request, 'operations/site.html',context)    

def sites(request):
    sites = Site.objects.all()
    context = {'sites':sites}
    return render(request, 'operations/sites.html',context)

def es_delete(request,site_id):
    docs = (Document.objects.filter(site_id=site_id).filter(isUsed__gt=0)
                    .values_list('id',flat=True))
    for d in docs:
        try:
            es.delete(d)
            print('es delete ' + str(d))
        except:
            pass
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def reset_to_zero(request,site_id):
    Document.objects.filter(site_id=site_id).update(isUsed=0)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def duplicate_filter(request,site_id):
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


def delete(request,site_id):
    if not request.user.is_staff:
        raise Http404
    else:
        Document.objects.filter(site_id=int(site_id)).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def tester(request,query='',testinggroup=1,page=1):
    context = {}
    if query:
        esquery = urllib.unquote_plus(query)
        if page == 0:
            page = 1
        if request.method == 'POST':
            TestingFormSet = formset_factory(TestingFormResult,extra=0)
            formset = TestingFormSet(request.POST,prefix='doc')
            if not formset.is_valid():
                return HttpResponse(str(formset.errors))

            if formset.is_valid():
                if TestingGroup.objects.filter(pk=testinggroup).count() == 0:
                    TestingGroup(id=testinggroup).save()
                docs = TestingResult.objects.filter(testinggroup=testinggroup).filter(searchterm=esquery)
                for form in formset:
                    document = int(form.cleaned_data['document'])
                    score = None

                    if form.cleaned_data['score'] == 0 or form.cleaned_data['score']:
                        score = int(form.cleaned_data['score'])
                    
                    doc = docs.filter(document_id=document)
                    if len(doc) > 0:
                        if score or score ==0:
                            doc.update(score=score)
                        else:
                            doc.delete()
                    elif score or score ==0:
                        TestingResult(searchterm=esquery,
                                testinggroup_id=testinggroup,
                                document_id=document,
                                score=score).save()
        
        context = es.search(esquery,100,100*(int(page)-1))
        TestingFormSet = formset_factory(TestingFormResult,extra=0)
        
        form_list= []
        scores = TestingResult.objects.filter(searchterm=esquery).filter(testinggroup_id=testinggroup)
        count = 1
        for r in context['result_list']:
            d = int(r['id'].decode('utf-8')) 
            f = {'document': d}
            s = scores.filter(document_id=d)
            if len(s) >0:
                score = s[0].score
            else:
                score = None
            f.update({'score': score})
            r.update({'count': count})
            count = count + 1
            form_list.append(f)
    
        formset = TestingFormSet(initial=form_list,prefix='doc')
        list = zip(formset, context['result_list'])
        context.update({'formset':formset})
        context.update({'list':list})
        context.update({'last_search':esquery})
        context.update({'testinggroup':testinggroup})
        context.update({'page':page})
        context.update({'linklist':pager(100,int(context['result_count']),page,10)})
    return render(request, 'operations/tester.html',context)

def document(request,doc_id):
    import HTMLParser
    doc = Document.objects.get(pk=doc_id)
    context = {            
            #'html': re.sub('\n','<br>',doc.document_html),
            'html': '<code>' + re.sub('\n','</code>\n<code>',cgi.escape(indexer.get_body_html(doc.document_html))) + '</code>',
            'parsed_text' : '<br>'.join(indexer.text_parse(doc.document_html))
            }

    return render(request, 'operations/document.html',context)


def pager(size,result_count,page,linkcount):
    lastpage = int(result_count/size) + 1
    if lastpage < linkcount:
        return range(1,lastpage+1)
    elif int(page) < linkcount/2:
        return range(1,linkcount+1)
    elif int(page) > (lastpage - (linkcount/2)):
        return range(lastpage-linkcount,lastpage+1)
    else:
        return range(int(page)-(linkcount/2),int(page)+(linkcount/2)+1)
        
