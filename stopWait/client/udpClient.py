#! /bin/python
from socket import *
import sys
import re
import os

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
    send_handshake(clientSocket)
    send_packets(textFname,clientSocket)

def send_handshake(clientSocket):
    message = "Starting handshake"
    clientSocket.sendto(message, serverAddr)
    modifiedMessage, clientAddrPort = clientSocket.recvfrom(2048)
    print "Message from %s is: %s" % (repr(clientAddrPort), modifiedMessage)

def send_packets(textFname, clientSocket):
    size= os.path.getsize(textFname)
    counter= 0
    i=0
    k=100
    message = ""
    with open(textFname, 'r') as inputFile:
        while counter < size:
            if (size - counter < 100):
                k = size - counter
            while i < k:
                message += inputFile.read(counter)
                i += 1
                counter += 1
            i = 0
        clientSocket.sendto(message, serverAddr)
        print "Message from %s is: %s" % (repr(serverAddr), message)


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
