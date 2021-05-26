import hashlib
from Crypto.Cipher import AES
import base64
import os

class Encrypt():
    '''encrypts sensitive data for querying with database'''
    def __init__(self, password, salt):
        self.key = self.__keyFromPassword(password,bytes.fromhex(salt))

    def __pad(self,s): 
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size) 

    def __unpad(self,data):
        return data[0:-ord(data[-1])]
    
    def __cipher(self,cipherKey,iv='0'*16):
        return AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv)
    
    def __bloatString(self,string, salt):
        # return hashlib.pbkdf2_hmac('sha512', string.encode('utf8') , salt , 100000).hex()
        return hashlib.pbkdf2_hmac('sha512', string.encode('utf8') , salt , 100000)

    
    def __keyFromPassword(self,password,salt):
        # bloated_string = self.__bloatString(password, base64.b64encode(os.urandom(16)))
        bloated_string = self.__bloatString(password, salt)

        return {"cipherKey": bloated_string[:24]," hashingSalt": bloated_string[24:]}
    
    def encrypt(self,data):
        # return self.__cipher(self.key["cipherKey"]).encrypt(self.__pad(data)).hex()
        return self.__cipher(self.key["cipherKey"]).encrypt(self.__pad(data))

    def decrypt(self,hex_data):
        # data = bytes.fromhex(hex_data)
        data = hex_data
        return self.__unpad(self.__cipher(self.key["cipherKey"]).decrypt(data).decode())
    
