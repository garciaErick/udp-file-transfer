#! /bin/python
from socket import *

# default params
serverAddr = ("", 50001)

import sys

def usage():
    print "usage: %s [--serverPort <port>]" % sys.argv[0]
    sys.exit(1)

# TODO:
# def split_into_packets():

# TODO:
# def retransmit_on_duplicate():

# At least one side must implement retransmit-on-timeout; otherwise a lost packet leads to deadlock as the sender
# and the receiver both wait forever. The other side must implement at least one of retransmit-on-duplicate or
# retransmit-on-timeout; usually the former alone. If both sides implement retransmit-on-timeout with different
# timeout values, generally the protocol will still work.

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]
        del args[0]
        if sw == "--serverPort":
            serverAddr = ("", int(args[0]))
            del args[0]
        else:
            print "unexpected parameter %s" % args[0]
            usage()
except:
    usage()

print "binding datagram socket to %s" % repr(serverAddr)

def receive_handshake(serverSocket):
    message, clientAddrPort = serverSocket.recvfrom(2048)
    if (message == "Trying to start handshake from client"):
        modifiedMessage = "Acknowledging handshake from server"
        print modifiedMessage
        serverSocket.sendto(modifiedMessage, clientAddrPort)
        print "Successfully initiated communication with client"



def put_method():
    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(serverAddr)
    receive_handshake(serverSocket)
    print "ready to receive"
    with open("stopWait/server/putFromClient.txt", 'w') as outputFile:
        while 1:
            try:
                message, clientAddrPort = serverSocket.recvfrom(2048)
                outputFile.write(message + "\n")
                outputFile.flush()
            finally:
                message = "Successfully made put request"
                serverSocket.sendto(message, clientAddrPort)

put_method()
