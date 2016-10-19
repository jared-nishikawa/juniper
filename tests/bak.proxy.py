#!/usr/bin/python


from twisted.internet import reactor
from twisted.web import http
from twisted.internet import protocol

class ClientRequest(http.Request):
    def __init___(self, channel, reactor=reactor):
        Request.__init__(self, channel)
        self.reactor = reactor
    def process(self):
        print self.method
        print self.uri
        print self.clientproto

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.transport.write("Hello")

    def dataReceived(self, data):
        print "Server said:", data
        self.transport.loseConnection()


class proxyProtocol(http.HTTPChannel):
    requestFactory = ClientRequest

class EchoProtocol(protocol.Protocol):
    def dataReceived(self, data):
        print data
        self.transport.write(data)

class EchoFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return EchoProtocol()


class ProxyProtocol(protocol.Protocol):
    def dataReceived(self, data):
        print data
        self.transport.write(data)

class ProxyFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return EchoProtocol()


def main():

    reactor.listenTCP(8080, MyFactory())
    reactor.run()

if __name__ == "__main__":
    main()
