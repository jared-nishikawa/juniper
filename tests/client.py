#!/usr/bin/python

from twisted.internet import ssl,reactor
from twisted.internet.protocol import ClientFactory, Protocol

class EchoClient(Protocol):
    def connectionMade(self):
        print "Connection made"
        self.transport.write("GET / HTTP/1.1\r\nHost: www.amazon.com\r\n\r\n")

    def dataReceived(self, data):
        print "Data:\n", data
        self.transport.loseConnection()

class EchoClientFactory(ClientFactory):
    protocol = EchoClient
    def clientConnectionFailed(self, connector, reason):
        print "Connection failed -- goodbye!"
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print "Connection lost -- goodbye!"
        reactor.stop()

if __name__ == "__main__":
    factory = EchoClientFactory()
    reactor.connectSSL('www.amazon.com', 443, factory, ssl.ClientContextFactory())
    reactor.run()
