#! /bin/python
from socket import *

# default params
serverAddr = ("", 50001)

import sys

def usage():
    print "usage: %s [--serverPort <port>]" % sys.argv[0]
    sys.exit(1)


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
    message = "Yeah handshake"
    serverSocket.sendto(message, clientAddrPort)



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
