import os
from cryptography.fernet import Fernet

# key = Fernet.generate_key()
key = os.environ['fernet-key']
fernet = Fernet(key)

def encrypt(info):
    encMessage = fernet.encrypt(info.encode())
    return encMessage

def decrypt(info):
    decMessage = fernet.decrypt(info).decode()
    return decMessage