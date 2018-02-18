#! /bin/python
from socket import *
import sys
import re
import os


def usage():
    print "usage: %s [--serverAddr host:port]" % sys.argv[0]


def get_method(file_name):
    print("Creating file: ")
    with open(file_name, 'w') as inputFile:  # Add to the dictionary the words found in the file.
        inputFile.write('i play to win')


def put_method(file_name):
    print("Initializing PUT from client")
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    send_handshake(clientSocket)
    send_packets(file_name, clientSocket)


def send_handshake(clientSocket):
    message = "Trying to start handshake from client"
    print message
    clientSocket.sendto(message, serverAddr)
    modifiedMessage, clientAddrPort = clientSocket.recvfrom(2048)
    if (modifiedMessage == "Acknowledging handshake from server"):
        print "Successfully initiated communication with server\n"
    else:
        print "Failed to innitiate trying again\n"
        # Send on timeout
        sys.exit(1)

        # print "Message from %s is: %s" % (repr(clientAddrPort), modifiedMessage)


def send_packets(file_name, clientSocket):
    size = os.path.getsize(file_name)
    counter = 0
    i = 0
    k = 100
    message = ""
    with open(file_name, 'r') as inputFile:
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


# TODO:
# def retransmit_on_timeout():


# default params
serverAddr = ('localhost', 50000)
protocol = ""
file_name = ""

# TODO: research on this for better args parsing https://docs.python.org/3.3/library/argparse.html
try:
    args = sys.argv[1:]
    while args:
        sw = args[0]
        del args[0]
        if sw == "--serverAddr":
            addr, port = re.split(":", args[0])
            del args[0]
            serverAddr = (addr, int(port))
        elif sw == "--protocol" or sw == "-p":
            protocol = args[0]
            del args[0]
        elif sw == "--file_name" or sw == "-f":
            file_name = args[0]
            del args[0]
        else:
            print "unexpected parameter %s" % args[0]
            usage()

    if protocol == "put":
        put_method("putTestFile.txt")
    elif protocol == "get":
        get_method("getTestFile.txt")
    else:
        print "Invalid protocol: %s" % protocol
        usage()
except:
    print "An exception ocurred"
    usage()
    sys.exit(1)
