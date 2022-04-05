import hashlib
from Crypto.Cipher import AES
import base64
import os

class Encrypter():
    '''encrypts sensitive data for querying with database'''
    def __init__(self, app=None):
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """This is used to set up encrypter for your app object.

        :param app: the Flask app object with proper configuration.
        """
        self.key = self.__keyFromPassword(app.config['DB_ENCRYPTION_KEY'],bytes.fromhex(app.config['DB_ENCRYPTION_SALT']))
    
    def __pad(self,s):
        '''returns a padded unicode string for AES 192-bit block encryption''' 
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size) 

    def __unpad(self,data):
        '''unpad string after decoding'''
        return data[0:-ord(data[-1])]
    
    def __cipher(self,cipherKey,iv='0'*16):
        return AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv.encode('utf8'))
    
    def __bloatString(self,string, salt):
        '''expands string using hashing, to ensure it's long enough so that it can supply both
        a cipher key and a hashing salt'''
        # return hashlib.pbkdf2_hmac('sha512', string.encode('utf8') , salt , 100000).hex()
        return hashlib.pbkdf2_hmac('sha512', string.encode('utf8') , salt , 100000)

    
    def __keyFromPassword(self,password,salt):
        # bloated_string = self.__bloatString(password, base64.b64encode(os.urandom(16)))
        bloated_string = self.__bloatString(password, salt)

        return {"cipherKey": bloated_string[:24]," hashingSalt": bloated_string[24:]}
    
    def encrypt(self,data):
        '''encrypts a string'''
        # return self.__cipher(self.key["cipherKey"]).encrypt(self.__pad(data)).hex()
        # print(type(self.__pad(data).encode('utf8')))
        # test = self.__pad(data).encode('utf8')
        # print('type:', type(test))
        return self.__cipher(self.key["cipherKey"]).encrypt(self.__pad(data).encode('utf8'))

    def decrypt(self,hex_data):
        '''decrypts a byte sequence into it's string equivalent'''
        # data = bytes.fromhex(hex_data)
        data = hex_data
        return self.__unpad(self.__cipher(self.key["cipherKey"]).decrypt(data).decode())
    
