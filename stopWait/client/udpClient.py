#! /bin/python
from socket import *
import sys
import re
import os

# default params
serverAddr = ('localhost', 50000)
clientSocket = socket(AF_INET, SOCK_DGRAM)
protocol = ""
file_name = ""


def usage():
    print "usage: %s [--serverAddr host:port]" % sys.argv[0]



def get_method(file_name):
    print "Initializing GET from server"
    # clientSocket = socket(AF_INET, SOCK_DGRAM)
    send_handshake(clientSocket)
    recieve_packets(file_name, clientSocket)


def recieve_packets(file_name, clientSocket):
    with open("getFromServer.txt", 'w') as outputFile:
        while 1:
            try:
                message, serverAddrPort = clientSocket.recvfrom(2048)
                if message != "Finished!":
                    print message + "NUMBERS    "
                    outputFile.write(message + "\n")
                    outputFile.flush()
                else:
                    print "Done!"
                    sys.exit(1)

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


def get_method(file_name):
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    file_name = "stopWait/client/getFromServer.txt"
    with open(file_name, 'w') as outputFile:
        while 1:
            try:
                print "fuck da pliz"
                packet, serverAddrPort = clientSocket.recvfrom(2048)
                outputFile.write(packet + "\n")
                outputFile.flush()
            finally:
                message = "Successfully made get request"
                clientSocket.sendto(message, serverAddrPort)


def put_method(file_name):
    print("Initializing PUT from client")
    send_packets(file_name, clientSocket)


def send_handshake(clientSocket):
    message = "Trying to start handshake from client"
    print message
    clientSocket.sendto(message, serverAddr)
    modifiedMessage, clientAddrPort = clientSocket.recvfrom(2048)
    if (modifiedMessage == "Acknowledging handshake from server"):
        print "Successfully initiated communication with server\n"
    else:
        print modifiedMessage
        # Send on timeout
        sys.exit(1)

def send_protocol_and_fname(clientSocket, protocol, file_name):
    print "Starting protocol: %s, file: %s" % (protocol.upper(), file_name)
    messageToAwknoledge = protocol + " " + file_name
    clientSocket.sendto(messageToAwknoledge, serverAddr)
    modified_message, serverAddrPort = clientSocket.recvfrom(2048)
    # print "Modified message from %s is <%s>" % (repr(serverAddrPort), modified_message)
    if (modified_message == "Acknowledging handshake from server"):
        print "Successfully initiated communication with server\n"
    else:
        # print "Failed to innitiate trying again\n"
        print modified_message
        # Send on timeout
        sys.exit(1)
    print "Initializing PUT from client"
    # send_packets(file_name, clientSocket)
    packets_to_send = split_into_packets(file_name)
    for packet in packets_to_send:
        clientSocket.sendto(packet, serverAddr)
    print "Sucessfully finished PUT request"


def split_into_packets(file_name):
    size = os.path.getsize(file_name)
    counter = 0
    i = 0
    k = 100
    message = ""
    packets = list()
    with open(file_name, 'r') as inputFile:
        while counter < size:
            if (size - counter < 100):
                k = size - counter
            while i < k:
                message += inputFile.read(counter)
                i += 1
                counter += 1
            i = 0
        packets.append(message)
    return packets


# TODO:
# def retransmit_on_timeout():

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

        if protocol.lower() == "put":
            send_protocol_and_fname(clientSocket, protocol, file_name)
            put_method(file_name)
        elif protocol.lower() == "get":
            send_protocol_and_fname(clientSocket, protocol, file_name)
            get_method(file_name)
        else:
            print "unexpected parameterr %s" % args[0]
            print "Invalid protocol: %s" % protocol
            usage()
    except Exception as e:
        print "An exception ocurred " + "\n" + str(e)
        usage()
        sys.exit(1)


main()
