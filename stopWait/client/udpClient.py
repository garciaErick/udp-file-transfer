#! /bin/python
from socket import *

import sys
import re
import os
import time
import signal
import timeit
# default params
serverAddr = ('localhost', 50000)
clientSocket = socket(AF_INET, SOCK_DGRAM)
protocol = ""
file_name = ""


def usage():
    print "usage: %s [--serverAddr host:port -p protocol -f file_name]" % sys.argv[0]


# Sending protocol and file name to server and starting communication
def send_protocol_and_fname(clientSocket, protocol, file_name):
    print "Starting protocol from client: %s, file: %s" % (protocol.upper(), file_name)
    message = protocol + " " + file_name
    clientSocket.sendto(message, serverAddr)
    modified_message, serverAddrPort = clientSocket.recvfrom(2048)
    if (modified_message == "Acknowledging handshake from server"):
        print "1. Successfully initiated communication with server\n"
    else:
        print "Failed to innitiate trying again\n"
        sys.exit(1)


# Splitting file into packets of 100B
def split_into_packets(file_name):
    size = os.path.getsize("stopWait/client/" + file_name)
    counter = 0
    k = 100
    i = 0
    packets = list()
    with open(file_name, 'rb') as inputFile:
        while counter < size:
            message = ""
            message += inputFile.read(k)
            packets.append(message)
            counter += k
            i += 1
    packets.append("Finished!")
    return packets


# The signal is used for the retransmit-on-timeout
def signal_handler(signum, frame):
    raise Exception("timeout")


def put_method(file_name):
    print("2. Initializing PUT from client\n")
    modified_message = ""
    packets = split_into_packets(file_name)
    i = 0
    for packet in packets:
        clientSocket.sendto(packet, serverAddr)
        modified_message, serverAddrPort = clientSocket.recvfrom(2048)
        signal.signal(signal.SIGALRM, signal_handler)
        while (modified_message != "Recieved packet " + str(i)):
            try:
                if (modified_message == "Received last packet"):
                    print "3. Successfully processed PUT request. Terminating client..."
                    sys.exit(0)
                print packet
                print modified_message
                signal.alarm(6)
                modified_message, serverAddrPort = clientSocket.recvfrom(2048)
            except Exception as e:  # if a timeout occurs it will try to retransmit
                if e.message == "timeout":
                    print "timeout ocurred"
                    clientSocket.sendto(packet, serverAddr)
        i += 1
        modified_message = ""
    print "Sucessfully finished PUT request"


def get_method(file_name, clientSocket):
    print("2. Initializing GET from client\n")
    i = 0
    with open("stopWait/client/" + file_name, 'w') as outputFile:
        while 1:
            timeStart = timeit.default_timer()
            packet, serverAddrPort = clientSocket.recvfrom(2048)
            if packet == "Finished!":
                print "3. Successfully processed GET request. Terminating client..."
                clientSocket.sendto("Received last packet", serverAddrPort)
                sys.exit(1)
            # time.sleep(4)
            print "Packet took : "  + str(timeit.default_timer()- timeStart ) + " seconds"
            clientSocket.sendto("Recieved packet " + str(i), serverAddrPort)
            outputFile.write(packet)
            outputFile.flush()
            i += 1


def main():
    try:
        # Parsing script args
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

        # Sendig protocol to server and starting protocol on client side
        clientSocket = socket(AF_INET, SOCK_DGRAM)
        if protocol.lower() == "put":
            send_protocol_and_fname(clientSocket, protocol, file_name)
            put_method(file_name)
        elif protocol.lower() == "get":
            send_protocol_and_fname(clientSocket, protocol, file_name)
            get_method(file_name, clientSocket)
        else:
            print "unexpected parameterr %s" % args[0]
            print "Invalid protocol: %s" % protocol
            usage()
    except Exception as e:
        print "An exception ocurred " + "\n" + str(e)
        usage()
        sys.exit(1)


main()
