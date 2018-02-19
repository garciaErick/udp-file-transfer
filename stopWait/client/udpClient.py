#! /bin/python
from socket import *
import sys
import re
import os


def usage():
    print "usage: %s [--serverAddr host:port]" % sys.argv[0]


def get_method(file_name):
    # clientSocket = socket(AF_INET, SOCK_DGRAM)
    # send_handshake(clientSocket)
    recieve_packets(file_name, clientSocket)


def recieve_packets(file_name, clientSocket):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    with open("stopWait/client/getFromServer.txt", 'w') as outputFile:
        while 1:
            try:
                print "fuck da pliz"
                message, serverAddrPort = clientSocket.recvfrom(2048)
                outputFile.write(message + "\n")
                outputFile.flush()
            finally:
                message = "Successfully made get request"

def put_method(file_name):
    print("Initializing PUT from client")
    send_packets(file_name, clientSocket)


# def send_handshake(clientSocket):
#     message = "Trying to start handshake from client"
#     print message
#     clientSocket.sendto(message, serverAddr)
#     modifiedMessage, clientAddrPort = clientSocket.recvfrom(2048)
#     if (modifiedMessage == "Acknowledging handshake from server"):
#         print "Successfully initiated communication with server\n"
#     else:
#         print modifiedMessage
#         # Send on timeout
#         sys.exit(1)

def send_protocol_and_fname(clientSocket, protocol, file_name):
    print "Starting protocol: %s, file: %s" % (protocol.upper(), file_name)
    message = protocol + " " + file_name
    clientSocket.sendto(message, serverAddr)
    modified_message, serverAddrPort = clientSocket.recvfrom(2048)
    print modified_message
    if (modified_message == "Acknowledging handshake from server"):
        print "Successfully initiated communication with server\n"
    else:
        print "Failed to innitiate trying again\n"
        # Send on timeout
        sys.exit(1)

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

#TODO:
#def split_into_packets(file_name):


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

    clientSocket = socket(AF_INET, SOCK_DGRAM)
    if protocol.lower() == "put":
        send_protocol_and_fname(clientSocket, protocol, file_name)
        put_method(file_name)
    elif protocol.lower() == "get":
        send_protocol_and_fname(clientSocket, protocol, file_name)
        get_method(file_name)
    else:
        print "Invalid protocol: %s" % protocol
        usage()
except Exception as e:
    print "An exception ocurred " + "\n"  + str(e)
    usage()
    sys.exit(1)
