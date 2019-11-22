# Sample code for Multi-Threaded Server
#Python 3
# Usage: python3 UDPserver3.py
#coding: utf-8
from socket import *
import threading
import time
import datetime as dt
import sys

from login import authentication,getusername

serverPort = int(sys.argv[1])
block_duration = int(sys.argv[2])
timeout = int(sys.argv[3])

#Server will run on this port

t_lock=threading.Condition()
#will store clients info in this list
clients=[]
onlineUsers=[]
blacklist=[]
chances={}
# would communicate with clients after every second
UPDATE_INTERVAL=2

def timeoutT(addr,name):
    global timeout
    time.sleep(timeout)
    clients.remove(addr)
    
    send_message("timeout",addr)
    

def blocking(username):
    global blacklist
    global block_duration    
    blacklist.append(username)
    time.sleep(block_duration)
    blacklist.remove(username)
    

def send_message(string,address):
    global clientSocket
    clientSocket.sendto(string.encode(),address)

def recv_handler():
    global t_lock
    global clients
    global clientSocket
    global serverSocket

    global blacklist
    serverMessage = ''
    print('Server is ready for service')
    while(1):

        message, clientAddress = serverSocket.recvfrom(2048)
        #received data from the client, now we know who we are talking with
        message = message.decode()
        message.strip()
        
        #get lock as we might me accessing some shared data structures
        with t_lock:
            
            # login authentication
            if (clientAddress not in clients):
                    print(message)
                    # check if user in black list
                    username = getusername(message)
                    if (username in blacklist):
                        serverMessage = "Your account is blocked due to multiple login failures. Please try again later"
                        
                    # authentication successfully
                    elif authentication(message):                        
                        clients.append(clientAddress)
                        timeout_t = threading.Thread(target=timeoutT,args=[clientAddress,username])
                        timeout_t.daemon=True
                        timeout_t.start()
                        
                        serverMessage = "Login successfull"

                        # clear error histry
                        if username in chances:
                            chances.pop(username)

                        # add a timeout thread for this user                        

                    # authentication failed
                    else:
                        if username in chances.keys():
                            chances[username] +=1
                        else :
                            chances[username] = 1
                        serverMessage = "Invalid Password. "                        
                        # failed more then 3 times
                        if (chances[username] >= 3):
                            chances.pop(username)
                            serverMessage += " Your account has been blocked. Please try again later."
                            block_t=threading.Thread(target=blocking,args=[username])
                            block_t.daemon=True
                            block_t.start()
                        else:
                            serverMessage += "Please try again"

                    send_message(serverMessage,clientAddress)

            # already login
            else :                
                currtime =dt.datetime.now()
                date_time = currtime.strftime("%d/%m/%Y, %H:%M:%S")

                print('Received request from', clientAddress[0], 'listening at', clientAddress[1], ':', message, 'at time ', date_time)
                if(message == 'logout'):
                    #check if client already subscribed or not
                    if(clientAddress in clients):
                        clients.remove(clientAddress)
                        serverMessage="Logout successfully"
                    else:
                        serverMessage="Already logout"
                else:
                    serverMessage="Unknown command, add more implementation here"
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
