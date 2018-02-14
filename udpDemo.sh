#!/bin/bash
pkill python

printf "Starting UDP Server\n"
python stopWait/server/udpServer.py &
printf "Success\n\n"

printf "Starting UDP Proxy\n"
python proxy/udpProxy.py &
printf "Success\n\n"

sleep 1

printf "Starting UDP Client\n"
python stopWait/client/udpClient.py
printf "Success\n\n"

pkill python