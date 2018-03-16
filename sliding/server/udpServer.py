#! /bin/python
from socket import *

import sys
import os
import time
import signal
import timeit
# default params
serverAddr = ("", 50001)


def usage():
    print "usage: %s [--serverPort <port>]" % sys.argv[0]
    sys.exit(1)





def split_into_packets(file_name):
    size = os.path.getsize(file_name)
    counter = 0
    k = 100
    i = 0
    packets = list()
    with open(file_name, 'rb') as inputFile:
        while counter < size:
            message = ""
            # if (size - counter < 100):
            #     k = size - counter
            message += inputFile.read(k)
            packets.append(message)
            counter += k
            i += 1

    # print len(packets)
    packets.append("Ending Communication!")
    return packets



# def split_into_packets(file_name):
#     size = os.path.getsize(file_name)
#     counter = 0
#     i = 0
#     k = 100
#     packets = list()
#     with open(file_name, 'rb') as inputFile:
#         while counter < size:
#             message = ""
#             if (size - counter < 100):
#                 k = size - counter
#             while i < k:
#                 message += inputFile.read(1)
#                 i += 1
#                 counter += 1
#                 # print "i" + str(i)
#                 # print "k" + str(k)
#                 # print "Inside loop " + message
#
#             packets.append(message)
#             i = 0
#             inputFile.flush()
#     i = 0
#     for packet in packets:
#         print str(i) + ": " + packet
#         i += 1
#     return packets


# TODO:
# def retransmit_on_duplicate():

# At least one side must implement retransmit-on-timeout; otherwise a lost packet leads to deadlock as the sender
# and the receiver both wait forever. The other side must implement at least one of retransmit-on-duplicate or
# retransmit-on-timeout; usually the former alone. If both sides implement retransmit-on-timeout with different
# timeout values, generally the protocol will still work.

def signal_handler(signum, frame):
    raise Exception("timeout")

def receive_protocol_and_fname(serverSocket):
    signal.signal(signal.SIGALRM, signal_handler)
    message, clientAddrPort = serverSocket.recvfrom(2048)
    modified_message = "Acknowledging handshake from server"
    protocol, file_name , sliding_size = message.split(" ")
    window_size = int(sliding_size)
    protocol = protocol.lower()
    while(1):
        try:
            serverSocket.sendto(modified_message, clientAddrPort)
            if protocol == "put":
                break
            elif protocol == "get":
                break
            signal.alarm(2)
            message, clientAddrPort = serverSocket.recvfrom(2048)
            protocol, file_name , sliding_size = message.split(" ")
            window_size = int(sliding_size)
            protocol = protocol.lower()
        except Exception as e:
            if e.message == "timeout":
                print protocol
                serverSocket.sendto(modified_message, clientAddrPort)
    if protocol == "put":
        put_method(file_name, window_size)
    elif protocol == "get":
        get_method(file_name, clientAddrPort, window_size)

def get_method(file_name, clientAddrPort,window_size):
    print "ready to send"
    packets = split_into_packets(file_name)
    i=0
    currentSize = 0
    temp = 0
    counter =0
    while counter < len(packets)-1:
        signal.signal(signal.SIGALRM, signal_handler)
        currentSize = 0
        temp =0
        # serverSocket.sendto(packet, clientAddrPort)
        # modified_message, clientAddrPort = serverSocket.recvfrom(2048)
        while currentSize < window_size:
            leIterativePackets = list()
            while( (temp + counter) < (len (packets)-1) and temp < window_size):
                leIterativePackets.append(packets[temp+counter])
                temp +=1
            print leIterativePackets
            for packet in leIterativePackets:
                serverSocket.sendto(packet,clientAddrPort)
                modified_message, clientAddrPort = serverSocket.recvfrom(2048)
                while ( modified_message != "Recieved packet " + str(i) ):
                    try:
                        # print "Modified message : " + modified_message
                        # print modified_message
                        signal.alarm(2)
                        modified_message, clientAddrPort = serverSocket.recvfrom(2048)
                    except Exception as e:
                        if e.message == "timeout":
                            print "timeout lol"
                            serverSocket.sendto(packet, clientAddrPort)
                i+=1
                modified_message=""
            currentSize+=1
        counter += window_size
    serverSocket.sendto("Ending Communication!", clientAddrPort)
    print "Sucessfully finished GET request"
    # serverSocket.sendto("Ending Communication!",clientAddrPort)

def put_method(file_name,window_size):
    with open("sliding/server/" + file_name, 'w') as outputFile:
        i=0
        k = 0
        currentSize = 0
        packetNumber =0
        while 1:
            currentSize=0
            startTime = timeit.default_timer()
            while currentSize < window_size:
                packet, clientAddrPort = serverSocket.recvfrom(2048)
                if packet == "Ending Communication!":
                    print "Done!"
                    serverSocket.sendto("Recieved packet " + str(i), clientAddrPort)
                    sys.exit(1)
                serverSocket.sendto("Recieved packet " + str(i), clientAddrPort)
                currentSize +=1
                i +=1
                print str(i) + " " +  packet
                print "Time taken for packet: " + str(i) + " was "+ str(timeit.default_timer() - startTime ) + " seconds"
                outputFile.write(packet)
            outputFile.flush()


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
