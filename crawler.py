#coding:utf-8
#siddontang@gmail.com

import time

from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop

from greenlet_tornado import *

from urllister import URLLister

AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

class Crawler:
    def __init__(self, beginUrl):
        self._beginUrl = beginUrl
        self._urlTasks = []
        self._urlMarked = {}
        self._imgs = []
        self._maxTaskNum = 10
        self._taskNum = 0
        self._ioloop = ioloop.IOLoop()
        
    def run(self, depth):
        self._crawl(self._beginUrl, depth)

        self._ioloop.add_timeout(time.time() + 1, self._checkTask)
        
        self._ioloop.start()

    def getImgs(self):
        return self._imgs

    def _checkStop(self):
        if not self._urlTasks and self._taskNum == 0:
            self._ioloop.stop()
            return False

        return True
            
    def _checkTask(self):
        if not self._checkStop():
            return
        
        newTaskNum = self._maxTaskNum - self._taskNum

        for i in xrange(newTaskNum):
            try:
                (url, depth) = self._urlTasks.pop(0)
                self._crawl(url, depth)
            except:
                break

        self._ioloop.add_timeout(time.time() + 1, self._checkTask)
    
    @greenlet_asynchronous
    def _crawl(self, url, depth):
        if depth == 0:
            return

        if url in self._urlMarked:
            return

        self._urlMarked[url] = True

        if self._taskNum > self._maxTaskNum:
            self._urlTasks.append((url, depth))
            return

        self._taskNum = self._taskNum + 1

        response = greenlet_fetch(self._ioloop, url)

        if response.error:
            print 'Error', response.error, url
        else:
            data = response.body

            lister = URLLister()
            lister.feed(data)

            urls = lister.getUrls()
            imgs = lister.getImgs()

            self._imgs.extend(imgs)

            for newUrl in urls:
                self._crawl(newUrl, depth - 1)

        self._taskNum = self._taskNum - 1
        self._checkStop()
        
if __name__ == '__main__':
    mainPage = Crawler("http://www.qq.com")
    mainPage.run(1)

    imgs = mainPage.getImgs()

    for img in imgs:
        print img
        
