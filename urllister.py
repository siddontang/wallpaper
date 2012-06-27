#coding:utf-8
#siddontang@gmail.com

import traceback

from sgmllib import SGMLParser

class URLLister(SGMLParser):
    def __init__(self):
        SGMLParser.__init__(self)
        self._clear()


    def feed(self, data):
        try:
            SGMLParser.feed(self, data)
        except Exception:
            print 'SGMLParser error %s' % traceback.format_exc() 
        
    def reset(self):
        SGMLParser.reset(self)
        self._clear()

    def getUrls(self):
        return self._urls

    def getImgs(self):
        return self._imgs
        

    def _clear(self):
        self._urls = []
        self._imgs = []
    
    def start_a(self, attrs):  
        href = [ v for k,v in attrs if k=="href" and v.startswith("http")]  
        if href:  
            self._urls.extend(href)
      
    def start_img(self, attrs):  
        src = [ v for k,v in attrs if k=="src" and v.startswith("http") ]  
        if src:  
            self._imgs.extend(src)  


if __name__ == '__main__':
    import urllib2

    try:
        f = urllib2.urlopen('http://www.qq.com').read()
        urlLister = URLLister()
        urlLister.feed(f)

        urls = urlLister.getUrls()
        imgs = urlLister.getImgs()

        for img in imgs:
            print img
    except urllib2.URLError, e:
        print e.reason
