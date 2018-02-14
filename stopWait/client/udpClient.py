#! /bin/python
from socket import *
import sys
import re

# default params
serverAddr = ('localhost', 50000)


def usage():
    print "usage: %s [--serverAddr host:port]" % sys.argv[0]
    sys.exit(1)


def get_method(textFname):
    print("Creating file: ")
    with open(textFname, 'w') as inputFile:  # Add to the dictionary the words found in the file.
        inputFile.write('i play to win')


def put_method(textFname):
    print("Initializing PUT from client")
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    with open(textFname, 'r') as inputFile:
        for line in inputFile:
            line = line.strip()
            message = line
            clientSocket.sendto(message, serverAddr)
        modifiedMessage, serverAddrPort = clientSocket.recvfrom(2048)
        print "Message from %s is: %s" % (repr(serverAddrPort), modifiedMessage)


try:
    args = sys.argv[1:]
    while args:
        sw = args[0]
        del args[0]
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0])
            del args[0]
            serverAddr = (addr, int(port))
        else:
            print "unexpected parameter %s" % args[0]
            usage()
except:
    usage()

put_method("putTestFile.txt")
