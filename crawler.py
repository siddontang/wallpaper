#coding:utf-8
#siddontang@gmail.com

import time

from taskpool import TaskPool
from urllister import URLLister

class Crawler:
    def __init__(self, beginUrl):
        self._beginUrl = beginUrl
        self._urlTasks = []
        self._urlMarked = {}
        self._imgs = []
        self._taskpool = TaskPool(10)
        
    def run(self, depth):
        self._crawl(self._beginUrl, depth)
        self._taskpool.run()

    def getImgs(self):
        return self._imgs

    def _crawl(self, url, depth):
        if depth == 0:
            return

        if url in self._urlMarked:
            return

        self._urlMarked[url] = True

        def callback(response):
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

        self._taskpool.spawn(url, callback)
        
if __name__ == '__main__':
    mainPage = Crawler("http://www.qq.com")
    mainPage.run(1)

    imgs = mainPage.getImgs()

    for img in imgs:
        print img
        
