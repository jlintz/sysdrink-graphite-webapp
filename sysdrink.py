#!/usr/bin/python

import sys
import logging
import time
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
from socket import socket

CARBON_SERVER = '127.0.0.1'
CARBON_PORT = 2003

class DrinkHandler(tornado.web.RequestHandler):
    def get(self, drink):
        sock = socket()
        try:
          sock.connect( (CARBON_SERVER,CARBON_PORT) )
        except:
          logging.error("Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT })
        now = int( time.time() )
        message = "sysdrink.drink.%s 1 %d\n" % (drink, now)
        logging.info(message)
        sock.sendall(message)
        self.finish("Drank 1 %s at %d" % (drink, now))

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.finish('hai')

class Application(tornado.web.Application):
    def __init__(self):
        app_settings = {
            'debug': True,
            'autoescape': None,
        }

        handlers = [
            (r"/$", MainHandler),
            (r"/drink/(.*)", DrinkHandler),
        ]

        tornado.web.Application.__init__(self, handlers, **app_settings)

if __name__ == "__main__":
    tornado.options.define("port", default=8080, type=int)
    tornado.options.parse_command_line()
    logging.info("starting up on %d" % (tornado.options.options.port))
    http_server = tornado.httpserver.HTTPServer(request_callback=Application())
    http_server.listen(tornado.options.options.port, address="127.0.0.1")
    tornado.ioloop.IOLoop.instance().start()
