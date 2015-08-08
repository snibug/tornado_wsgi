#!/usr/bin/python
#
# 2014 write by @sungho

from tornado import web
from tornado.escape import native_str
from tornado.wsgi import HTTPRequest

import gevent.pywsgi
import httplib
import logging
import socket
import sys
import tornado.wsgi


SO_REUSEPORT = 15
REUSE_ADDR = 'reuse_addr'


class ReusePortMixIn(object):
  """"""
  def get_listener(self, address, backlog=None, family=None):
    sock = socket.socket(family=family)
    sock.setblocking(0)

    try:
      sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
      logging.warning('fail to change socket option: SO_REUSEADDR')

    try:
      sock.setsockopt(socket.SOL_SOCKET, SO_REUSEPORT, 1)
    except:
      logging.warning('fail to open socket option: SO_REUSEPORT')

    try:
      sock.bind(address)
    except socket.error:
      ex = sys.exc_info()[1]
      if getattr(ex, 'strerror', None) is not None:
        ex.strerror = ex.strerror + ': ' + repr(address)
      logging.warning(ex.strerror)

      sys.exit(1)

    if backlog is None:
      if getattr(self, 'backlog', None) is not None:
        backlog = int(self.backlog)
      else:
        backlog = 50
    sock.listen(backlog)

    return sock


class HTTPServer(ReusePortMixIn, gevent.pywsgi.WSGIServer):
  """"""
  handler_class = gevent.pywsgi.WSGIHandler


class HTTPApplication(tornado.wsgi.WSGIApplication):
  """"""


class HTTPRequestHandler(tornado.web.RequestHandler):
  """"""
