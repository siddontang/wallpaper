#coding:utf-8
#siddontang@gmail.com

class Config:
    def __init__(self):
        self._url = ''
        
        self._cachePath = './cache'
        self._downImagePath = './cache/image'
        self._urlCacheDB = './cache/urlcache.db'

        self.getCachePath = lambda : self._cachePath
        self.getDownImagePath = lambda : self._downImagePath
        self.getUrlCacheDB = lambda : self._urlCacheDB
        
        self.getMainUrl = lambda : self._url

    def setMainUrl(self, url):
        self._url = url
        
    
