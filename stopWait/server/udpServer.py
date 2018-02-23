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
    packets.append("Finished!")
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

def get_method(file_name, clientAddrPort):
    print "ready to send"
    packets_to_send = split_into_packets(file_name)
    i=0
    modified_message= ""
    for packet in packets_to_send:
        signal.signal(signal.SIGALRM, signal_handler)
        serverSocket.sendto(packet, clientAddrPort)
        modified_message, clientAddrPort = serverSocket.recvfrom(2048)
        print packet
        while ( modified_message != "Recieved packet " + str(i) ):
            try:
                print "Modified message : " + modified_message
                if((modified_message != "Recieved packet " + str(len(packets_to_send)-1))):
                    print "YAAAAAAAAAAA1AY"
                    sys.exit(0)
                print modified_message
                signal.alarm(5)
                modified_message, clientAddrPort = serverSocket.recvfrom(2048)
            except Exception as e:
                if e.message == "timeout":
                    print "timeout lol"
                    serverSocket.sendto(packet, clientAddrPort)
        # serverSocket.sendto(packet, clientAddrPort)
        # time.sleep(.100)
        i+=1
        modified_message=""
    print "Sucessfully finished GET request"
    # serverSocket.sendto("Finished!",clientAddrPort)

def put_method(file_name):
    with open("stopWait/server/putFromClient.txt", 'w') as outputFile:
        i=0
        k = 0
        while 1:
                # if k == 2:
                #     time.sleep(5)
                #     k=0
                packet, clientAddrPort = serverSocket.recvfrom(2048)
                print packet
                if packet == "Finished!":
                    print "Done!"
                    serverSocket.sendto("Recieved packet " + str(i), clientAddrPort)
                    sys.exit(1)
                outputFile.write(packet)
                serverSocket.sendto("Recieved packet " + str(i), clientAddrPort)
                outputFile.flush()
                k +=1
                i +=1


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
