#coding:utf-8
#siddontang@gmail.com

import os
import time
import traceback
import hashlib
from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop

from greenlet_tornado import *
import tornado.curl_httpclient

AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

class ImageDown:
    def __init__(self, urls, location, urlCache, interval = 10):
        self._urls = list(set(urls))
        self._location = location

        if not os.path.exists(location):
            os.mkdir(location)

        self._interval = interval
        self._taskNum = 0
        self._maxTaskNum = 10
        self._cache = urlCache

        self._ioloop = ioloop.IOLoop()

    def setInterval(self, interval):
        self._interval = interval

    def getInterval(self):
        return self._interval
        
    def run(self):
        self._runTasks()
        
        self._ioloop.add_timeout(time.time() + self._interval, self._checkTask)

        self._ioloop.start()
                

    def _checkTask(self):
        if not self._urls and self._taskNum == 0:
            self._ioloop.stop()
            return
            
        self._runTasks()

        self._ioloop.add_timeout(time.time() + self._interval, self._checkTask)
                
    def _runTasks(self):
        newTaskNum = self._maxTaskNum - self._taskNum

        for i in xrange(newTaskNum):
            try:
                url = self._urls.pop(0)
                self._down(url)
            except Exception, e:
                print e
                break
        
    @greenlet_asynchronous
    def _down(self, url):
        if self._cache.get(url):
            return
        
        self._taskNum = self._taskNum + 1
        
        response = greenlet_fetch(self._ioloop, url)
        if response.error:
            print 'Error', response.error, url
        else:
            data = response.body
            self._writeImage(url, data)
            
        self._taskNum = self._taskNum - 1    
        
    def _writeImage(self, url, data):
        try:
            fileName = (url.split('/')[-1])
            fileExt = os.path.splitext(fileName)[-1]
            
            fileName = hashlib.md5(data).hexdigest() + fileExt

            fullName = os.path.join(self._location, fileName)

            if not os.path.exists(fullName):
                with open(fullName, 'wb') as f:
                    f.write(data)

            self._cache.set(url, fullName)
                    
        except:
            print 'write image %s error %s' % (url, traceback.format_exc())


if __name__ == '__main__':
    from crawler import Crawler
    from urlcache import UrlCache

    mainPage = Crawler("http://www.qq.com")
    mainPage.run(1)

    imgs = mainPage.getImgs()

    cache = UrlCache('urlcache.db')
    imgDown = ImageDown(imgs, './download',cache,1)
    imgDown.run()

    cache.save()
