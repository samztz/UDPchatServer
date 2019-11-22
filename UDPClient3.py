#Python 3
#Usage: python3 UDPClient3.py localhost 12000
#coding: utf-8
from socket import *
import time
import threading
import sys


#Server would be running on the same host as Client
serverName = sys.argv[1]
serverPort = int(sys.argv[2])
online = False
username =''
password =''
receivedMessage=''
UPDATE_INTERVAL=1


t_lock=threading.Condition()

clientSocket = socket(AF_INET, SOCK_DGRAM)

def send_message(string):
    global serverName
    global serverPort
    clientSocket.sendto(string.encode(),(serverName, serverPort))

def closeConnection():
    global clientSocket
    global serverAddress
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


def send_handler():
    global t_lock
    global online

    while(online):
        with t_lock:
            msg = input("> ")
            send_message(msg)
            t_lock.notify()


def recv_handler():
    global t_lock
    global clientSocket
    global online
    
    #wait for the reply from the server
    while (online):
        receivedMessage, serverAddress = clientSocket.recvfrom(2048)
        receivedMessage = receivedMessage.decode()        
        print(receivedMessage)
        if (receivedMessage == "Logout successfully"):            
            online = False
            sys.exit(0)
        elif(receivedMessage=="timeout"):
            online = False
            sys.exit(0)
        else:
            time.sleep(UPDATE_INTERVAL)
            

msg = gatherLogininfo()
send_message(msg)

# main loop
while(1): 
    receivedMessage, serverAddress = clientSocket.recvfrom(2048)
    receivedMessage = receivedMessage.decode()
    print(receivedMessage)

        # case successful
    if (receivedMessage =='Login successfull'):
        online = True
        send_thread=threading.Thread(name="SendHandler", target = send_handler)
        send_thread.daemon=True
        send_thread.start()

        recv_thread = threading.Thread(name="RecvHandler", target= recv_handler)
        recv_thread.daemon=True
        recv_thread.start()
        break

        # case failed < 3 times
    elif (receivedMessage =='Invalid Password. Please try again'):
        #  retype message
        print("Retry username and password..")
        msg = gatherLogininfo()
        send_message(msg)
        #  case blocked
    else:
        break

while True:
    time.sleep(0.1)
    if(not online):
        sys.exit(0)
