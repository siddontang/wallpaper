
import greenlet
import tornado.httpclient
import tornado.web
from functools import wraps

def greenlet_fetch(request, **kwargs):
    gr = greenlet.getcurrent()
    assert gr.parent is not None, "greenlet_fetch() can only be called (possibly indirectly) from a RequestHandler method wrapped by the greenlet_asynchronous decorator."

    def callback(response):
        gr.switch(response)

    http_client = tornado.httpclient.AsyncHTTPClient()
    http_client.fetch(request, callback, **kwargs)

    response = gr.parent.switch()

    return response


def greenlet_asynchronous(wrapped_method):
    @wraps(wrapped_method)
    def wrapper(self, *args, **kwargs):

        def greenlet_base_func():
            wrapped_method(self, *args, **kwargs)

        gr = greenlet.greenlet(greenlet_base_func)
        gr.switch()

    return wrapper
