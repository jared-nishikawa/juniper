#!/usr/bin/python


from twisted.internet import reactor
from Proxy import ProxyProtocol, ProxyFactory
import argparse

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
            '--port',
            type=int,
            required=False,
            default=8080,
            help="specify port for the proxy to listen on (defaults to 8080)")
    parser.add_argument('-l',
            '--log',
            help="log POST requests",
            action="store_true",
            default=False)
    args = parser.parse_args()
    PORT = args.port
    LOG = args.log

    print "Juniper proxy started on port", str(PORT) + "..."
    if LOG:
        print "Writing POST requests to juniper.log"
    reactor.listenTCP(PORT, ProxyFactory(LOG))
    reactor.run()

if __name__ == "__main__":
    main()
