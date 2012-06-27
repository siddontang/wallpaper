#coding:utf-8
#siddontang@gmail.com

import os
import time
import traceback

from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop

from greenlet_tornado import greenlet_fetch
from greenlet_tornado import greenlet_asynchronous

AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")


class ImageDown:
    def __init__(self, urls, location, interval = 10):
        self._urls = list(set(urls))
        self._location = location

        if not os.path.exists(location):
            os.mkdir(location)

        self._interval = interval
        self._taskNum = 0
        self._maxTaskNum = 10
        
    def run(self):
        ioloop.IOLoop.instance().add_timeout(time.time() + self._interval, self._checkTask)

        self._runTasks()
        
        ioloop.IOLoop.instance().start()

    def _checkTask(self):
        if not self._urls:
            ioloop.IOLoop.instance().stop()
    
        ioloop.IOLoop.instance().add_timeout(time.time() + self._interval, self._checkTask)

        self._runTasks()

    def _runTasks(self):
        if not self._urls:
            ioloop.IOLoop.instance().stop()

        newTaskNum = self._maxTaskNum - self._taskNum

        for i in xrange(newTaskNum):
            try:
                url = self._urls.pop(0)
                self._down(url)
            except:
                break
        
    @greenlet_asynchronous
    def _down(self, url):
        self._taskNum = self._taskNum + 1
        
        response = greenlet_fetch(url)
        if response.error:
            print 'Error', response.error, url
        else:
            data = response.body
            self._writeImage(url, data)
            
        self._taskNum = self._taskNum - 1    

    def _writeImage(self, url, data):
        try:
            fileName = url.split('/')[-1]
            
            while True:
                fullName = os.path.join(self._location, fileName)
                if os.path.exists(fullName):
                    fileName = '%d_%s' % (int(time.time()), fileName)
                    fullName = os.path.join(self._location, fileName)
                else:
                    break

            with open(fullName, 'wb') as f:
                f.write(data)
        except:
            print 'write image %s error %s' % (url, traceback.format_exc())


if __name__ == '__main__':
    from crawler import Crawler
    
    mainPage = Crawler("http://www.qq.com")
    mainPage.run(1)

    imgs = mainPage.getImgs()

    imgDown = ImageDown(imgs, './download')
    imgDown.run()
