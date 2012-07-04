#coding:utf-8
#siddontang@gmail.com

import traceback

from tornado.httpclient import AsyncHTTPClient
from tornado import ioloop
from tornado.curl_httpclient import CurlAsyncHTTPClient
AsyncHTTPClient.configure(CurlAsyncHTTPClient)

class TaskPool:
    def __init__(self, maxClients):
        self._ioloop = ioloop.IOLoop()
        self._httpClient = AsyncHTTPClient(self._ioloop, maxClients)
        self._taskNum = 0
        
    def run(self):
        self._check()
        self._ioloop.start()

    def spawn(self, request, callback, **kwargs):
        def wapped(response):
            self._taskNum -= 1
            try:
                callback(response)
            except:
                print 'spwan error:', traceback.format_exc()
                pass
                
        self._taskNum += 1
        self._httpClient.fetch(request, wapped, **kwargs)

    def _check(self):
        def callback():
            if self._taskNum == 0:
                self._ioloop.stop()

            return self._check()
                
        self._ioloop.add_callback(callback)
