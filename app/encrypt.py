import hashlib
from Crypto.Cipher import AES
import base64
import os

class Encrypt():
    '''encrypts sensitive data for querying with database'''
    def __init__(self, password):
        self.key = self.__keyFromPassword(password)

    def __pad(self,s): 
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size) 

    def __unpad(self,data):
        return data[0:-ord(data[-1])]
    
    def __cipher(self,cipherKey,iv='0'*16):
        return AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv)
    
    def __bloatString(self,string, salt):
        return hashlib.pbkdf2_hmac('sha512', string.encode('utf8') , salt , 100000).hex()
    
    def __keyFromPassword(self,password):
        bloated_string = self.__bloatString(password, base64.b64encode(os.urandom(16)))
        return {"cipherKey": bloated_string[:32]," hashingSalt": bloated_string[32:]}
    
    def encrypt(self,data):
        return self.__cipher(self.key["cipherKey"]).encrypt(self.__pad(data)).hex()

    def decrypt(self,hex_data):
        data = bytes.fromhex(hex_data)
        return self.__unpad(self.__cipher(self.key["cipherKey"]).decrypt(data).decode())
    
