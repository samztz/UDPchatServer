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
def closeConnection():
    global clientSocket
    message='Unsubscribe'
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    clientSocket.close()

msg = input("Subscribe: ")

# username = input("Username: ")
# password = input("Password: ")
# msg = username + ' ' + password

send_message(msg)

#wait for the reply from the server
receivedMessage, serverAddress = clientSocket.recvfrom(2048)
if (receivedMessage.decode()=='Login successfull'):
    print("done")
    closeConnection()

if (receivedMessage.decode()=='Subscription successfull'):
    #Wait for 10 back to back messages from server
    for i in range(10):
        receivedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(receivedMessage.decode())
#prepare to exit. Send Unsubscribe message to server

else :
    closeConnection()
# Close the socket
