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

from taskpool import TaskPool

class ImageDown:
    def __init__(self, urls, location, urlCache):
        self._urls = list(set(urls))
        self._location = location

        if not os.path.exists(location):
            os.mkdir(location)

        self._cache = urlCache

        self._taskpool = TaskPool(10)
        
    def addUrls(self, urls):
        self._urls.extend(list(set(urls)))
        
        
    def run(self):
        urls = []
        urls, self._urls = self._urls, urls

        for url in urls:
            self._down(url)

        self._taskpool.run()
        
    def _down(self, url):
        if self._cache.get(url):
            return
        
        def callback(response):
            if response.error:
                print 'Error', response.error, url
            else:
                data = response.body
                self._writeImage(url, data)

        self._taskpool.spawn(url, callback)
        
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

    cache = UrlCache('./cache/urlcache.db')
    imgDown = ImageDown(imgs, './download',cache)
    imgDown.run()

    cache.save()
