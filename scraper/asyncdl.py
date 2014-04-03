from pprint import pformat
from Queue import Queue

from twisted.internet import reactor
import twisted.internet.defer
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet import error 

import sys
sys.path.append('/home/ec2-user/bblio/build/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'
import chardet
import datetime
from time import sleep

from search.models import Document
update_group = 1

class PrinterClient(Protocol):
    def __init__(self, whenFinished,doc_info,charset):
        self.whenFinished = whenFinished
        self._data = ''
        self._doc = doc_info
        self._charset = charset

    def dataReceived(self, bytes):
        self._data += bytes

    def connectionLost(self, reason):
        if reason.check(twisted.web.client.ResponseDone):
            if self._charset == 'ASCII':
                self._data = self._data.decode('ascii').encode('utf-8')
            elif self._charset != 'UTF-8':
                self._data = self._data.decode(chardet.detect(self._data)['encoding']).encode('utf-8')

            self.whenFinished.callback(handleFinish(self._data, self._doc))
        else:   
            print '[Finish] Connection: %s', reason.getErrorMessage()
            self.whenFinished.callback(handleFinish('', self._doc))

def handleFinish(r,doc_info):
    doc = Document.objects.get(pk=doc_info[0])
    try:
        if len(r) == 0:
            doc.response_code = 1000
        else:
            doc.document_html = r.decode('utf-8')
            doc.update_group = 1
    except:
        doc.response_code = 999
    finally:
        doc.lastupdate = datetime.datetime.now()
        doc.save()
        doc = None
    print '[Finish] Handle: %s' % str(doc_info[0])


def handleResponse(r,doc_info):
    print "[code=%s] %s" % (r.code, doc_info)

    charset = ''
    try:
        charset = r.headers.getRawHeaders('content-type')[0].split('; ')[1].split('=')[1]
    except:
        pass

    whenFinished = twisted.internet.defer.Deferred()
    doc = Document.objects.get(pk=doc_info[0])
    p = PrinterClient(whenFinished,doc_info,charset)
    r.deliverBody(p)
    doc.response_code = r.code
    doc.save(update_fields=['response_code'])
    doc = None
    return whenFinished

def handleError(reason):
    reason.printTraceback()
    print 'Handle Error: %s', reason.getErrorMessage()
    #reactor.stop()

def getPage(doc_info,id):
    print "[Requesting] (%s) %s" % (str(id),doc_info[1],)
    d = Agent(reactor).request('GET', doc_info[1].encode('ascii'), \
            Headers({'User-Agent': ['twisted']}), None)

    d.addCallback(handleResponse, doc_info)
    d.addErrback(handleError)
    sleep(0.5)
    return d

semaphore = twisted.internet.defer.DeferredSemaphore(24)
dl = list()

rando = Document.objects.exclude(update_group=1).filter(isUsed=0).order_by('?'). \
        values_list('id', 'urlAddress')

for id, doc_info in enumerate(rando):
    dl.append(semaphore.run(getPage, doc_info,id))

dl = twisted.internet.defer.DeferredList(dl)
dl.addCallbacks(lambda x: reactor.stop(), handleError)

reactor.run()
