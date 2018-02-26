# SLIDING WINDOW
Both the Proxy and the Server must be running before attempting a request. When a request is made to the server it will the client will send the protocol and file name which the server will parse to determine what to do. When sending or requesting a file either through the PUT or GET request, it will first split the file into packets of 100 Bytes.  It is different from the stop and wait as it sends a window size of packets all together then waits for the acknowledment from the server. Last but not least, both client and server implemented a retransmit-on-timeout with different timeout values in order for this to work where the first packet is resent and the others come after.

## Client
A client can begin a PUT or GET request
* A *PUT* request will send a file from the /sliding/client/ to the /sliding/server/ directory
* A *GET* request will receive a file from the /sliding/server/ in the /sliding/clients/ directory

## Testing the application
On the root directory there are sample scripts **getSlidingDemo.sh** and **putSlidingDemo.sh** you can just run those and you will run the application
or just run the following commands:

* *PUT* from client:
    * The following will insert sliding/client/testFileFromClient.txt into sliding/server/testFileFromClient.txt
~~~~
python proxy/udpProxy.py &
python sliding/server/udpServer.py &
python sliding/client/udpClient.py -p PUT -f testFileFromClient.txt
~~~~

* *GET* from client
    * The following will insert sliding/server/testFileFromServer.txt into sliding/client/testFileFromServer.txt
~~~~
python proxy/udpProxy.py &
python sliding/server/udpServer.py &
python sliding/client/udpClient.py -p GET -f testFileFromServer.txt
~~~~

**Note** when sending files it will split these into packets of 100 bytes, and when sending a file
