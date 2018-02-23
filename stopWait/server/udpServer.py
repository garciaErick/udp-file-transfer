#! /bin/python
from socket import *

import sys
import os
import time
import signal

# default params
serverAddr = ("", 50001)


def usage():
    print "usage: %s [--serverPort <port>]" % sys.argv[0]
    sys.exit(1)


# Receiving protocol and file name from client and acting accordingly
def receive_protocol_and_fname(serverSocket):
    message, clientAddrPort = serverSocket.recvfrom(2048)
    modified_message = "Acknowledging handshake from server"

    protocol, file_name = message.split(" ")
    serverSocket.sendto(modified_message, clientAddrPort)

    protocol = protocol.lower()
    if protocol == "put":
        put_method(file_name)
    elif protocol == "get":
        get_method(file_name, clientAddrPort)
    else:
        sys.exit(1)


# Splitting file into packets of 100B
def split_into_packets(file_name):
    size = os.path.getsize("stopWait/server/" + file_name)
    counter = 0
    k = 100
    i = 0
    packets = list()
    with open("stopWait/server/" + file_name, 'rb') as inputFile:
        while counter < size:
            message = ""
            message += inputFile.read(k)
            packets.append(message)
            counter += k
            i += 1
    packets.append("Finished!")
    return packets


# Used for timeout
def signal_handler(signum, frame):
    raise Exception("timeout")


def put_method(file_name):
    print "1. Server started PUT request"
    with open("stopWait/server/" + file_name, 'w') as outputFile:
        i = 0
        k = 0
        while 1:
            # The following was used to test timeout
            # if k == 2:
            #     time.sleep(5)
            #     k=0
            packet, clientAddrPort = serverSocket.recvfrom(2048)
            if packet == "Finished!":
                print "\n2.Server finished PUT request"
                serverSocket.sendto("Received last packet", clientAddrPort)
                return

            outputFile.write(packet)
            serverSocket.sendto("Recieved packet " + str(i), clientAddrPort)
            outputFile.flush()
            k += 1
            i += 1


def get_method(file_name, clientAddrPort):
    print "1. Server started processing GET request"
    packets_to_send = split_into_packets(file_name)
    i = 0
    modified_message = ""
    for packet in packets_to_send:
        signal.signal(signal.SIGALRM, signal_handler)
        serverSocket.sendto(packet, clientAddrPort)
        modified_message, clientAddrPort = serverSocket.recvfrom(2048)
        while (modified_message != "Recieved packet " + str(i)):
            try:
                if (modified_message == "Received last packet"):
                    print "\n2. Server finished GET request"
                    return
                print modified_message
                signal.alarm(5)
                modified_message, clientAddrPort = serverSocket.recvfrom(2048)
            except Exception as e:  # if a timeout occurs it will try to retransmit
                if e.message == "timeout":
                    print "timeout ocurred"
                    serverSocket.sendto(packet, clientAddrPort)
        i += 1
        modified_message = ""
    print "2. Sucessfully finished GET request"


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

while 1:
    print "================================================"
    print "Server Ready to start receiving"
    print "================================================"

    serverSocket = socket(AF_INET, SOCK_DGRAM)
    serverSocket.bind(serverAddr)
    receive_protocol_and_fname(serverSocket)

    print "================================================"
    print "Ended communication with client"
    print "================================================\n"
