import threading
import time

blacklist= set()
name = "samztz"

def blacklist_handler():
    global blacklist
    global name
    localName = name
    blacklist.append(name)
    print("adding: " + name + " a to the list ")
    time.sleep(2)
    blacklist.remove(localName)
    print("removing: " + localName)

blacklist = []
for i in range(2):
    t = threading.Thread(target=blacklist_handler)
    if (i==1):
        name = "James"
    t.start()

for i in range(5):
    print(blacklist)
    time.sleep(1)