#!env/bin/python

"""
Example txzmq client.

    ./pair.py --method=bind --endpoint=ipc:///tmp/sock

    ./pair.py --method=connect --endpoint=ipc:///tmp/sock
"""
import os
import socket
import sys
import time
import zmq
import random
from optparse import OptionParser

from twisted.internet import reactor


rootdir = os.path.realpath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.insert(0, rootdir)
os.chdir(rootdir)

from txzmq import ZmqEndpoint, ZmqFactory, ZmqPairConnection


parser = OptionParser("")
parser.add_option("-m", "--method", dest="method", help="0MQ socket connection: bind|connect")
parser.add_option("-e", "--endpoint", dest="endpoint", help="0MQ Endpoint")
parser.set_defaults(method="connect", endpoint="ipc:///tmp/txzmq-pc-demo")

(options, args) = parser.parse_args()

zf = ZmqFactory()
e = ZmqEndpoint(options.method, options.endpoint)
s = ZmqPairConnection(zf, e)

def produce():
    data = [str(time.time()), socket.gethostname(), options.method]
    print "producing %r" % data
    try:
        s.send(data)

    except zmq.error.Again:
        print "Skipping, other end of pair missing..."

    reactor.callLater(1 + random.randint(0, 3), produce)

def doPrint(message):
    print "consuming %r" % (message,)

reactor.callWhenRunning(reactor.callLater, 1, produce)

s.onReceive = doPrint

reactor.run()
