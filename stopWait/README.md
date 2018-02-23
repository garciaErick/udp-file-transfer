# Stop and wait
Both the Proxy and the Server must be running before attempting a request. When a request is made to the server it will the client will send the protocol and file name which the server will parse to determine what to do. When sending or requesting a file either through the PUT or GET request, it will first split the file into packets of 100 Bytes. Then the sender will need an ACK[packetNumber] before it can send the next packet. Last but not least, both client and server implemented a retransmit-on-timeout with different timeout values in order for this to work

## Client
A client can innitiate a PUT or GET request
* A *PUT* request will send a file from the /stopWait/client/ to the /stopWait/server/ directory
* A *GET* request will receive a file from the /stopWait/server/ in the /stopWait/clients/ directory

## Testing the application
On the root directory there are sample scripts **getStopAndWitDemo.sh** and **putStopAndWaitDemo.sh** you can just run those and you will run the application
or just run the following commands:

* *PUT* from client: 
    * The following will insert stopWait/client/testFileFromClient.txt into stopWait/server/testFileFromClient.txt 
~~~~
python proxy/udpProxy.py &
python stopWait/server/udpServer.py &
python stopWait/client/udpClient.py -p PUT -f testFileFromClient.txt
~~~~

* *GET* from client
    * The following will insert stopWait/server/testFileFromServer.txt into stopWait/client/testFileFromServer.txt 
~~~~
python proxy/udpProxy.py &
python stopWait/server/udpServer.py &
python stopWait/client/udpClient.py -p GET -f testFileFromServer.txt
~~~~

**Note** when sending files it will split these into packets of 100 bytes, and when sending a file 
