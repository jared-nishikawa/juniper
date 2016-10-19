#!/usr/bin/python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
This example demonstrates a very simple HTTP proxy.

Usage:
        $ python proxy.py

        Then configure your web browser to use localhost:8080 as a proxy, and visit a
        URL (This is not a SOCKS proxy). When browsing in this configuration, this
        example will proxy connections from the browser to the server indicated by URLs
        which are visited.

        See also logging-proxy.py for a proxy with additional features.
        """

from twisted.web import proxy, http
from twisted.internet import reactor



class ProxyProtocol(proxy.Proxy, http.Request):

    def dataReceived(self, data):
        print data
    
    def process(self):
        print self.method
        print self.uri
        print self.clientproto

class ProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return ProxyProtocol()

reactor.listenTCP(8080, ProxyFactory())
reactor.run()
