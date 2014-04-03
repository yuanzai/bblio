from pprint import pformat
from Queue import Queue

from twisted.internet import reactor
import twisted.internet.defer
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.web.client import getPage

import sys
sys.path.append('/home/ec2-user/bblio/build/')
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Build.settings'

from search.models import Document

rando = Document.objects.filter(isUsed=0)[:1] \
        .values_list('urlAddress',flat=True)

class PrinterClient(Protocol):
    def __init__(self, whenFinished):
        self.whenFinished = whenFinished
        self._data = ''

    def dataReceived(self, bytes):
        #print '##### Received #####\n%s' % (bytes,)
        self._data += bytes
        #print '##### Received #####\n'
        pass

    def connectionLost(self, reason):
        print 'Finished:', reason.getErrorMessage()
        self.whenFinished.callback(handleFinish(self._data))

def handleFinish(r):
    print('Finish')

def handleResponse(r):
    #print "version=%s\ncode=%s\nphrase='%s'" % (r.version, r.code, r.phrase)
    print "code=%s" % (r.code)
    #for k, v in r.headers.getAllRawHeaders():
        #print "%s: %s" % (k, '\n  '.join(v))
    whenFinished = twisted.internet.defer.Deferred()
    r.deliverBody(PrinterClient(whenFinished))
    return whenFinished

def handleError(reason):
    reason.printTraceback()
    reactor.stop()


"""
def printResponse(r):
    print '### Response ###\n %s', r

def printError(r):
    print(r)


print 'google'
getPage('http://google.com/').addCallbacks(
    callback=printResponse,
    errback=lambda error:(printError(error),reactor.stop()))

print 'yahoo'
getPage('http://yahoo.com/').addCallbacks(
    callback=printResponse,
    errback=lambda error:(printError(error),reactor.stop()))


reactor.run()
"""


def getPage(url):
    print "Requesting %s" % (url,)
    d = Agent(reactor).request('GET', url, Headers({'User-Agent': ['twisted']}), None)
    d.addCallbacks(handleResponse, handleError)
    return d

semaphore = twisted.internet.defer.DeferredSemaphore(2)
dl = list()

"""
for url in rando:
    dl.append(semaphore.run(getPage, url.encode('ascii')))
    pass
"""

dl.append(semaphore.run(getPage, 'http://google.com'))
dl.append(semaphore.run(getPage, 'http://dcnn.com'))
dl.append(semaphore.run(getPage, 'http://nytimes.com'))

dl = twisted.internet.defer.DeferredList(dl)
dl.addCallbacks(lambda x: reactor.stop(), handleError)

reactor.run()
