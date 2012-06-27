# Copyright (c) 2012 The greenlet-tornado Authors.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


# Author: Simon Radford <simon@mopub.com>
# Derived from this blog article:
#   http://blog.joshhaas.com/2011/06/marrying-boto-to-tornado-greenlets-bring-them-together/

"""
These functions allow you to seamlessly use Greenlet with Tornado.
This allows you to write code as if it were synchronous, and not worry about callbacks at all.
You also don't have to use any special patterns, such as writing everything as a generator.
"""

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
