#coding:utf-8
#siddontang@gmail.com

import os
import time
import traceback
import hashlib
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
        self._runTasks()
        
        ioloop.IOLoop.instance().add_timeout(time.time() + self._interval, self._checkTask)

        ioloop.IOLoop.instance().start()
                

    def _checkTask(self):
        if not self._urls and self._taskNum == 0:
            ioloop.IOLoop.instance().stop()
            return
            
        self._runTasks()

        ioloop.IOLoop.instance().add_timeout(time.time() + self._interval, self._checkTask)
                
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
            fileName = (url.split('/')[-1])
            fileExt = os.path.splitext(fileName)[-1]
            
            fileName = hashlib.md5(data).hexdigest() + fileExt

            fullName = os.path.join(self._location, fileName)

            if not os.path.exists(fullName):
                with open(fullName, 'wb') as f:
                    f.write(data)

        except:
            print 'write image %s error %s' % (url, traceback.format_exc())


if __name__ == '__main__':
    from crawler import Crawler
    
    mainPage = Crawler("http://www.qq.com")
    mainPage.run(1)

    imgs = mainPage.getImgs()

    imgDown = ImageDown(imgs, './download', 1)
    imgDown.run()
