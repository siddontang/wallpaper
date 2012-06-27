#coding:utf-8
#siddontang@gmail.com

from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop


from greenlet_tornado import greenlet_fetch
from greenlet_tornado import greenlet_asynchronous

from urllister import URLLister

AsyncHTTPClient.configure("tornado.curl_httpclient.CurlAsyncHTTPClient")

class Crawler:
    def __init__(self, beginUrl):
        self._beginUrl = beginUrl
        self._urlTasks = {}
        self._imgs = []
        
    def run(self, depth):
        self._crawl(self._beginUrl, depth)

        ioloop.IOLoop.instance().start()

    def getImgs(self):
        return self._imgs

    
    @greenlet_asynchronous
    def _crawl(self, url, depth):
        if depth == 0:
            return

        if url in self._urlTasks:
            return

        self._urlTasks[url] = True
        
        response = greenlet_fetch(url)
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

        self._urlTasks.pop(url)
        
        if not self._urlTasks:
            ioloop.IOLoop.instance().stop()

if __name__ == '__main__':
    mainPage = Crawler("http://www.qq.com")
    mainPage.run(2)

    imgs = mainPage.getImgs()

    for img in imgs:
        print img
        
