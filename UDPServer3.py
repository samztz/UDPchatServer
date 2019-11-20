# Sample code for Multi-Threaded Server
#Python 3
# Usage: python3 UDPserver3.py
#coding: utf-8
from socket import *
import threading
import time
import datetime as dt
import sys

from login import authentication

serverPort = int(sys.argv[1])
block_duration = sys.argv[2]
timeout = sys.argv[3]

#Server will run on this port

t_lock=threading.Condition()
#will store clients info in this list
clients=[]
blacklist=[]
# would communicate with clients after every second
timeout=False
UPDATE_INTERVAL=2;

def send_message(string,address):
    clientSocket.sendto(string.encode(),address)

def handleValidInput():

    #get lock as we might me accessing some shared data structures
    currtime = dt.datetime.now()
    date_time = currtime.strftime("%d/%m/%Y, %H:%M:%S")
    print('Received request from', clientAddress[0], 'listening at', clientAddress[1], ':', message, 'at time ', date_time)

    if(message == 'Subscribe'):
        #store client information (IP and Port No) in list
        clients.append(clientAddress)
        serverMessage="Subscription successfull"
    elif(message=='Unsubscribe'):
        #check if client already subscribed or not
        if(clientAddress in clients):
            clients.remove(clientAddress)
            serverMessage="Subscription removed"
        else:
            serverMessage="You are not currently subscribed"
    else:
        serverMessage="Unknown command, send Subscribe or Unsubscribe only"
    #send message to the client

def recv_handler():
    global t_lock
    global clients
    global clientSocket
    global serverSocket
    print('Server is ready for service')
    while(1):

        message, clientAddress = serverSocket.recvfrom(2048)
        #received data from the client, now we know who we are talking with
        message = message.decode()
        
        with t_lock:
            # login authentication
            if (clientAddress not in clients):
                    # TODO black list
                    # authentication
                    print(message)
                    if authentication(message):
                        clients.append(clientAddress)
                        send_message("Login successfull",clientAddress)
                    else:
                        send_message("Login~ failed",clientAddress)
                        t_lock.notify()
            # already login
            else :
                #get lock as we might me accessing some shared data structures
                currtime = dt.datetime.now()
                date_time = currtime.strftime("%d/%m/%Y, %H:%M:%S")
                print('Received request from', clientAddress[0], 'listening at', clientAddress[1], ':', message, 'at time ', date_time)

                if(message=='logout'):
                    #check if client already subscribed or not
                    if(clientAddress in clients):
                        clients.remove(clientAddress)
                        serverMessage="Logout successfully"
                    else:
                        serverMessage="Already logout"
                else:
                    serverMessage="Unknown command, send Subscribe or Unsubscribe only"
                #send message to the client
                serverSocket.sendto(serverMessage.encode(), clientAddress)
                #notify the thread waiting
                t_lock.notify()


def send_handler():
    global t_lock
    global clients
    global clientSocket
    global serverSocket
    global timeout
    #go through the list of the subscribed clients and send them the current time after every 1 second
    while(1):
        #get lock
        with t_lock:
            for i in clients:
                currtime =dt.datetime.now()
                date_time = currtime.strftime("%d/%m/%Y, %H:%M:%S")
                message='Current time is ' + date_time
                clientSocket.sendto(message.encode(), i)
                print('Sending time to', i[0], 'listening at', i[1], 'at time ', date_time)
            #notify other thread
            t_lock.notify()
        #sleep for UPDATE_INTERVAL
        time.sleep(UPDATE_INTERVAL)

#we will use two sockets, one for sending and one for receiving
clientSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
serverSocket.bind(('localhost', serverPort))

recv_thread=threading.Thread(name="RecvHandler", target=recv_handler)
recv_thread.daemon=True
recv_thread.start()

send_thread=threading.Thread(name="SendHandler",target=send_handler)
send_thread.daemon=True
send_thread.start()
#this is the main thread
while True:
    time.sleep(0.1)
