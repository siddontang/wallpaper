#coding:utf-8
#siddontang@gmail.com

import urllib2

from urllister import URLLister

class Page:
    def __init__(self, beginUrl):
        self._beginUrl = beginUrl
        self._imgs = []
        
    def travel(self, depth = 1):
        self._listUrls(self._beginUrl, depth)

    def getImgs(self):
        return self._imgs

    def _listUrls(self, url, depth):
        if depth == 0:
            return
        
        try:
            data = urllib2.urlopen(url).read()
            lister = URLLister()
            lister.feed(data)

            urls = lister.getUrls()
            imgs = lister.getImgs()

            self._imgs.extend(imgs)
            
            for url in urls:
                self._listUrls(url, depth - 1)
            
        except Exception, e:
            print e

        
if __name__ == '__main__':
    mainPage = Page("http://www.qq.com")
    mainPage.travel(1)

    imgs = mainPage.getImgs()

    for img in imgs:
        print img
        
