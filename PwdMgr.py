import sys

from cryptography.fernet import Fernet
key = b'pRmgMa8T0INjEAfksaq2aafzoZXEuwKI7wDe4c1F8AY='
cipher_suite = Fernet(key)

args = sys.argv
domain = ''
if len(args[1])<2:
    print('You have to input site url')
    exit(1)
domain = args[1]

def getPassword(ciphered_text):
    unciphered_text = (cipher_suite.decrypt(ciphered_text))
    plain_text_encryptedpassword = bytes(unciphered_text).decode("utf-8")
    return plain_text_encryptedpassword

def createPASS(passwd):
    passwd = str(passwd)
    password = passwd.encode('utf-8')
    ciphered_text = cipher_suite.encrypt(password)  # required to be bytes
    return ciphered_text

def writeByte(key, value):
    with open("password.txt", "wb") as myfile:
        key = createPASS(key)
        myfile.write(key)
        myfile.write(':'.encode('utf-8'))
        myfile.write(value)
        myfile.write('\n'.encode('utf-8'))

def appendByte(key, value):
    with open("password.txt", "ab") as myfile:
        myfile.write(createPASS(key))
        myfile.write(':'.encode('utf-8'))
        myfile.write(value)
        myfile.write('\n'.encode('utf-8'))

f = open('password.txt', 'rb')
lines = f.readlines()
f.close()

master_password = input('Enter Master Password:')
master_flag = False
for line in lines:
    line = line.replace(b'\n', b'')
    temp = line.split(b':')
    password = ''
    if len(temp)==2:
        password = temp[1]
    password = getPassword(password)
    key = getPassword(temp[0])
    if key=='master_password' and master_password==password:
        master_flag = True
        break

flag = False
password = ''

if master_flag:
    print('Loading database...')
    print('website: ' + domain)
    for line in lines:
        line = line.replace(b'\n', b'')
        temp = line.split(b':')
        password = ''
        if len(temp) == 2:
            password = temp[1]
        password = getPassword(password)
        key = getPassword(temp[0])
        if key == domain:
            flag = True
            break
    if flag:
        print('password: ' + password)
    else:
        print('No entry for  ', domain, ' creating new...')
        password = input('New entry - enter password for ' + domain + ':')
        password = createPASS(password)
        appendByte(domain, password)

else:
    print('No password database, creating...')
    master_password = createPASS(master_password)
    writeByte('master_password', master_password)
    print('Loading database...')
    print('No entry for  ', domain, ' creating new...')
    notice = 'New entry - enter password for ' + domain + ':'
    password = input(notice)
    password = createPASS(password)
    appendByte(domain, password)
    print('stored')
    f.close()

print('done')