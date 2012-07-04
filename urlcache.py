#coding:utf-8
#siddontang@gmail.com

import threading
import zlib
import cPickle as pickle
import os

class UrlCache:
    def __init__(self, dbfile):
        self._cache = {}
        self._rlock = threading.RLock()
        self._file = dbfile

        path = os.path.dirname(self._file)
        if not os.path.exists(path):
            os.makedirs(path)
            
        self.load()
        
    def set(self, url, fileName):
        self._cache[url] = fileName

    def get(self, url):
        return self._cache.get(url)

    def save(self):
        with self._rlock:
            try:
                with open(self._file, 'wb') as fp:
                    fp.write(zlib.compress(pickle.dumps(self._cache, True)))
            except:
                pass
            
    def load(self):
        with self._rlock:
            try:
                with open(self._file, 'rb') as fp:
                    self._cache = pickle.loads(zlib.decompress(fp.read()))
            except:
                self._cache = {}


if __name__ == '__main__':
    cache = UrlCache('./cache/urlcache.db')

    for url, fileName in cache._cache.iteritems():
        print url, fileName
