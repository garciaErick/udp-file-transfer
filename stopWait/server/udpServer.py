#! /bin/python
from socket import *

import sys
import os

# default params
serverAddr = ("", 50001)

def usage():
    print "usage: %s [--serverPort <port>]" % sys.argv[0]
    sys.exit(1)


def split_into_packets(file_name, clientAddrPort):
    # todo: estoy aqui
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
        serverSocket.sendto(message, clientAddrPort)
        print "Message from %s is: %s" % (repr(clientAddrPort), message)


# TODO:
# def retransmit_on_duplicate():

# At least one side must implement retransmit-on-timeout; otherwise a lost packet leads to deadlock as the sender
# and the receiver both wait forever. The other side must implement at least one of retransmit-on-duplicate or
# retransmit-on-timeout; usually the former alone. If both sides implement retransmit-on-timeout with different
# timeout values, generally the protocol will still work.


# def receive_handshake(serverSocket):
#     message, clientAddrPort = serverSocket.recvfrom(2048)
#     if (message == "Trying to start handshake from client"):
#         modifiedMessage = "Acknowledging handshake from server"
#         print modifiedMessage
#         serverSocket.sendto(modifiedMessage, clientAddrPort)
#         print "Successfully initiated communication with client"


def get_method(file_name, clientAddrPort):
    print "ready to send"
    split_into_packets(file_name,clientAddrPort)

def receive_protocol_and_fname(serverSocket):
    message, clientAddrPort = serverSocket.recvfrom(2048)
    modified_message = "Acknowledging handshake from server"
    serverSocket.sendto(modified_message, clientAddrPort)

    protocol, file_name = message.split(" ")
    serverSocket.sendto(modified_message, clientAddrPort)

    protocol = protocol.lower()
    if protocol == "put":
        put_method(file_name)
    elif protocol == "get":
        get_method(file_name, clientAddrPort)
    else:
        sys.exit(1)

    print protocol
    print file_name


def put_method(file_name):
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

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(serverAddr)
receive_protocol_and_fname(serverSocket)
# put_method()
# get_method()
