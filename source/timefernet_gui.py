import os
import time
import base64
import logging
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from fernet_gui import *




TTL = 30 #time to live en secondes




size_key=16


class TimeFernetGUI(FernetGUI):
    
    def __init__(self) -> None:
        super().__init__()


    def encrypt(self,message)->bytes:

        # déclaration de la méthode d'enchiffrement symétrique fernet
        fernet=Fernet(self._key)

	# récupération de l'heure actuelle
        t=int(time.time())
	
        # chiffrement du message selon la méthode fernet 

        encrypted=fernet.encrypt_at_time(bytes(message,'utf-8'),current_time=t)

        return encrypted
        
    def decrypt(self, msg) -> str:

        # décodage depuis base64
        dcdg=base64.b64decode(msg['data'])

        # on récupère l'heure actuelle afin de savoi si l'heure est valide
        t=int(time.time())

        decrypted=Fernet(self._key)

        try:
            # déchiffrement, si le msg est plus de 30secondes
            msg=decrypted.decrypt_at_time(dcdg,current_time=t,ttl=TTL)
            
            # msg dechiffré 
            return msg
         
        except InvalidToken as err:
            logging.error("Invalid Token")
            raise InvalidToken
        
        return str(message,"utf-8")

if __name__=="__main__":

    logging.basicConfig(level=logging.DEBUG)
    
    client=TimeFernetGUI()
    client.create()
    client.loop()
        