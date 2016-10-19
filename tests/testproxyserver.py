#!/usr/bin/python

from twisted.internet import reactor
from twisted.web import http

class RequestHandler(http.Request):
    resources = {"/": '<h1>Hello, world!</h1>'}
        
    def process(self):
        self.setHeader('Content-type', 'text/html')
        if self.resources.has_key(self.path):
            self.write(self.resources[self.path])
        else:
            self.setResponseCode(http.NOT_FOUND)
            self.write("<h1>Not found</h1>Sorry, no such resource")
        self.finish()

class MyHTTP(http.HTTPChannel):
    requestFactory = RequestHandler

class MyHTTPFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return MyHTTP()

reactor.listenTCP(8000, MyHTTPFactory())
reactor.run()
