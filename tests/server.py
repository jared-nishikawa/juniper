#!/usr/bin/python

from OpenSSL import SSL
from twisted.internet import ssl, reactor
from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver

from twisted.internet.protocol import Protocol

class TLSServer(Protocol):
    def dataReceived(self, data):
        print "received:", data
        if "CONNECT" in data:
            print "-- switching to TLS"
            #self.sendLine('READY')

            ctx = ServerTLSContext(
                    privateKeyFileName='en.wikipedia.org.key',
                    certificateFileName='en.wikipedia.org.crt',)
            


class ServerTLSContext(ssl.DefaultOpenSSLContextFactory):
    def __init__(self, *args, **kwargs):
        kwargs['sslmethod'] = SSL.TLSv1_METHOD
        ssl.DefaultOpenSSLContextFactory.__init__(self, *args, **kwargs)

if __name__ == '__main__':
    factory = ServerFactory()
    factory.protocol = TLSServer
    reactor.listenTCP(8080, factory)
    reactor.run()
