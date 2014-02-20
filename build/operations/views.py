from django.shortcuts import render, get_object_or_404
from search.models import Document, Site, TestingResult, TestingGroup
import es
import re
from django.http import HttpResponseRedirect, HttpResponse, Http404
from forms import TestingFormPage, TestingFormResult, AdminURLListForm, SiteForm
from django.forms.formsets import formset_factory
from django.forms.models import modelformset_factory
import urllib
from django.core.urlresolvers import reverse

def index(request):
    return render(request,'operations/index.html')

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
        #pure duplicate
        if len(docs.filter(urlAddress=url)) > 1:
            first_id = docs.filter(urlAddress=url)[0].id
            docs.filter(urlAddress=url).exclude(pk=first_id).update(isUsed=2)
        
        #https filter
        if url[:5] == 'https':
            url_http = url[:4] + url[5:]
            if len(docs.filter(urlAddress=url_http)) > 0:
                docs.filter(urlAddress=url).update(isUsed=3)
        
        #www filter
        if url[:11] == 'https://www':
            url_www = 'https://' + url[12:]
        elif url[:10] == 'http://www':
            url_www = 'http://' + url[11:]
        else:
            url_www = None

        if url_www:
            if len(docs.filter(urlAddress=url_www)) > 0:
                docs.filter(urlAddress=url_www).update(isUsed=4)
        #slash filter
        if url[-1:] == '/':
            url_slash = url[:-1]
            if len(docs.filter(urlAddress=url_slash)) > 0:
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
                    score = int(form.cleaned_data['score'])
                    doc = docs.filter(document_id=document)
                    if doc.count() > 0:
                        if score == 0:
                            doc.delete()
                        else:
                            doc.update(score=score)
                    elif score > 0:
                        TestingResult(searchterm=esquery,
                                testinggroup_id=testinggroup,
                                document_id=document,
                                score=score).save()
        
        context = es.search(esquery,100,100*(int(page)-1))
        TestingFormSet = formset_factory(TestingFormResult,extra=0)
        
        form_list= []
        scores = TestingResult.objects.filter(searchterm=esquery).filter(testinggroup_id=testinggroup)
        for r in context['result_list']:
            d = int(r['id'].decode('utf-8')) 
            f = {'document': d}
            s = scores.filter(document_id=d)
            if len(s) >0:
                score = s[0].score
            else:
                score = 0 
            f.update({'score': score})
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
        
