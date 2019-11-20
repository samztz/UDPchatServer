
def parceLoginInfo(string):
    return string.split()

# simple authentication function
def authentication(info):
    f = open('credentials.txt',mode ='r')
    while True:
        line = f.readline()
        line = line.strip()
        # TODO authenticate
        if (line == info):
            return True
        if not line:
            break
    f.close()
    return False
