
def getusername(string):
    return string.split(' ')[0]

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

# if (authentication('sam ztz')):
#     print('pass test')
# else :
#     print('fail test')
