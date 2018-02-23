#! /bin/python
from socket import *

import sys
import re
import os
import time
import signal
# default params
serverAddr = ('localhost', 50000)
clientSocket = socket(AF_INET, SOCK_DGRAM)
protocol = ""
file_name = ""


def usage():
    print "usage: %s [--serverAddr host:port]" % sys.argv[0]


def get_method(file_name,clientSocket):
    print("Initializing GET from client")
    i=0
    with open("stopWait/client/getFromServer.txt", 'w') as outputFile:
        while 1:
            packet, serverAddrPort = clientSocket.recvfrom(2048)
            print packet
            if packet == "Finished!":
                print "Done!"
                clientSocket.sendto("Recieved packet " + str(i), serverAddrPort)
                sys.exit(1)
            # time.sleep(4)
            clientSocket.sendto("Recieved packet " + str(i), serverAddrPort)
            outputFile.write(packet)
            outputFile.flush()
            i +=1

# def recieve_packets(file_name, clientSocket):



def send_protocol_and_fname(clientSocket, protocol, file_name):
    print "Starting protocol from client: %s, file: %s" % (protocol.upper(), file_name)
    message = protocol + " " + file_name
    clientSocket.sendto(message, serverAddr)
    modified_message, serverAddrPort = clientSocket.recvfrom(2048)
    if (modified_message == "Acknowledging handshake from server"):
        print "Successfully initiated communication with server\n"
    else:
        print "Failed to innitiate trying again\n"
        # TODO: Send on timeout
        sys.exit(1)

def signal_handler(signum, frame):
    raise Exception("timeout")

def put_method(file_name):
    print("Initializing PUT from client")
    modified_message=""
    packets = split_into_packets(file_name)
    i= 0
    for packet in packets:
        print packet
        clientSocket.sendto(packet, serverAddr)
        modified_message, serverAddrPort = clientSocket.recvfrom(2048)
        signal.signal(signal.SIGALRM, signal_handler)
        while ( modified_message != "Recieved packet " + str(i) ):
            try:
                if((modified_message != "Recieved packet " + str(len(packets)-1))):
                    print "YAAAAAAAAAAAAY"
                    sys.exit(0)
                print modified_message
                signal.alarm(3)
                modified_message, serverAddrPort = clientSocket.recvfrom(2048)
            except Exception as e:
                if e.message == "timeout":
                    print "timeout lol"
                    clientSocket.sendto(packet, serverAddr)
        # clientSocket.sendto(packet, serverAddr)
        i+=1
        modified_message=""
    print "Sucessfully finished PUT request"

# def resend_on_timeout(packet, clientSocket):


def send_protocol_and_fname(clientSocket, protocol, file_name):
    print "Starting protocol from client: %s, file: %s" % (protocol.upper(), file_name)
    message = protocol + " " + file_name
    clientSocket.sendto(message, serverAddr)
    modified_message, serverAddrPort = clientSocket.recvfrom(2048)
    if (modified_message == "Acknowledging handshake from server"):
        print "Successfully initiated communication with server\n"
    else:
        print "Failed to innitiate trying again\n"
        # Send on timeout
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
    packets.append("Finished!")
    return packets


# TODO:
def retransmit_on_timeout(packet):
    clientSocket.sendto(packet, serverAddr)



def main():
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
            get_method(file_name,clientSocket)
        else:
            print "unexpected parameterr %s" % args[0]
            print "Invalid protocol: %s" % protocol
            usage()
    except Exception as e:
        print "An exception ocurred " + "\n" + str(e)
        usage()
        sys.exit(1)


main()
