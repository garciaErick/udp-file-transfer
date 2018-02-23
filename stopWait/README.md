# Stop and wait
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
