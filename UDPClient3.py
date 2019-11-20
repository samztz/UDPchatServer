#Python 3
#Usage: python3 UDPClient3.py localhost 12000
#coding: utf-8
from socket import *
import sys

#Server would be running on the same host as Client
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
username =''
password =''

clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_message(string):
    clientSocket.sendto(string.encode(),(serverName, serverPort))

def closeConnection():
    global clientSocket
    message='logout'
    clientSocket.sendto(message.encode(),(serverName, serverPort))
    clientSocket.close()

    # gether usersname + password return as signle string format
def gatherLogininfo():
    global username
    global password
    username = input("Username: ")
    password = input("Password: ")
    return username + ' ' + password
# msg = input("Subscribe: ")
def handleInput():
    global receiveMassage
    global serverAddress
    while(1):

def recieving():
    global receiveMassage
    global serverAddress
    #wait for the reply from the server
    receivedMessage, serverAddress = clientSocket.recvfrom(2048)
    receivedMessage = receivedMessage.decode()

    # FIXME debugging ============
    print('Recieved: '+ receivedMessage)
    # ======================

msg = gatherLogininfo()
send_message(msg)

# main loop
while(1):
    if (receivedMessage =='Login successfull'):
        break;
    elif (receivedMessage =='Login failed'):
        #  retype message
        print("Retry username and password..")
        msg = gatherLogininfo()
        send_message(msg)
    else:
        handleInput():

if (receivedMessage =='Subscription successfull'):
    #Wait for 10 back to back messages from server
    for i in range(10):
        receivedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(receivedMessage.decode())
#prepare to exit. Send Unsubscribe message to server
else :
    closeConnection()
# Close the socket
