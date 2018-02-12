#! /bin/python
from socket import *

# default params
serverAddr = ('localhost', 50000)

import sys, re

def usage():
    print "usage: %s [--serverAddr host:port]"  % sys.argv[0]
    sys.exit(1)

def getMethod(textFname):
    print("Creating file: ")
    with open(textFname, 'w') as inputFile: #Add to the dictionary the words found in the file.
        inputFile.write('i play to win')

def putMethod(textFname):
    print("Uploading file")
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    with open(textFname, 'r') as inputFile:
        for line in inputFile:
            line= line.strip()
            message = line
            clientSocket.sendto(message, serverAddr)
            modifiedMessage, serverAddrPort = clientSocket.recvfrom(2048)
            print "Modified message from %s is <%s>" % (repr(serverAddrPort), modifiedMessage)

try:
    args = sys.argv[1:]
    while args:
        sw = args[0]; del args[0]
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0]); del args[0]
            serverAddr = (addr, int(port))
        else:
            print "unexpected parameter %s" % args[0]
            usage();
except:
    usage()

putMethod("testing.txt")
