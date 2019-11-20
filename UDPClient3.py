#Python 3
#Usage: python3 UDPClient3.py localhost 12000
#coding: utf-8
from socket import *
import sys

#Server would be running on the same host as Client
serverName = sys.argv[1]
serverPort = int(sys.argv[2])

clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_message(string):
    clientSocket.sendto(string.encode(),(serverName, serverPort))

username = input("Username: ")
password = input("Password: ")
msg = username + ' ' + password
print('sending: '+msg)
send_message(msg)


#wait for the reply from the server
receivedMessage, serverAddress = clientSocket.recvfrom(2048)

if (receivedMessage.decode()=='login successfull'):
    #Wait for 10 back to back messages from server
    for i in range(10):
        receivedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(receivedMessage.decode())
#prepare to exit. Send Unsubscribe message to server
else if():
else if():
else :
    message='Unsubscribe'
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    clientSocket.close()
# Close the socket
