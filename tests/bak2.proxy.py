#!/usr/bin/python


from twisted.internet import reactor
from twisted.web import http
from twisted.internet import protocol

HTTPMETHODS = ["GET", "HEAD", "POST", "PUT", "DELETE", "OPTIONS", "TRACE"]


def parseURL(url):
    tokens = url.split(':')
    newurl = ':'.join(tokens[1:])
    newurl = newurl.lstrip('/')
    tokens = newurl.split(':')
    if tokens[1:]:
        port = tokens[1].split('/')[0]
        tokens[1] = tokens[1].lstrip(port)
        port = int(port)
    else:
        port = 80
    newurl = ''.join(tokens)
    cut = newurl.index('/')
    host = newurl[:cut]
    path = newurl[cut:]
    return host,path,port

def makeHeader(method, path, proto):
    if not path:
        path = '/'
    payload = ' '.join([method,path,proto])
    return payload

def generateRequest(method, uri, proto, headers):
    host,path,port = parseURL(uri)
    header = makeHeader(method, path, proto)
    __request = [key + ': ' + headers[key] for key in headers.keys()]
    request = header + '\r\n' + '\r\n'.join(__request) + '\r\n\r\n'
    return host,path,port,request

class ProxyRequestHandler(http.Request):
    def process(self):
        print "*"*80
        print "BEGIN PROCESSING"
        method = self.method
        uri = self.uri
        proto = self.clientproto
        headers = self.getAllHeaders()
        if method == "CONNECT":
            print "HTTPS not implemented"
        elif method in HTTPMETHODS:
            host, path, port, packet = generateRequest(method, uri, proto, headers)
            print packet
            reactor.connectTCP(host, port, ForwardFactory(packet=packet))
        print "END PROCESSING"
        print "*"*80
        print "\n"*4

class ProxyProtocol(http.HTTPChannel):
    requestFactory = ProxyRequestHandler

class ProxyFactory(http.HTTPFactory):
    def buildProtocol(self, addr):
        return ProxyProtocol()

class Forward(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def connectionMade(self):
        self.transport.write(self.factory.packet)

    def dataReceived(self, data):


class ForwardFactory(protocol.ClientFactory):
    def __init__(self, packet=None):
        self.packet = packet

    def buildProtocol(self, addr):
        return Forward(self)


def main():

    reactor.listenTCP(8080, ProxyFactory())
    reactor.run()

if __name__ == "__main__":
    main()
