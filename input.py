import threading
import time

import sys

inputlist =[]

def readInput():
    inputTime = int(input("> "))

    print_t = threading.Thread(target=printInput,args=[inputTime])
    print_t.daemon = True
    print_t.start()

def printInput(bad):
    i=0
    while (i < bad):
        i+=1
        print(f"now {i} seconds")
        time.sleep(1)
    print("timeout")
    sys.exit(0)



read_t = threading.Thread(target=readInput)
read_t.daemon = True
read_t.start()

while(1):
    time.sleep(1)
    