import os
import base64
import hashlib
import logging
import dearpygui.dearpygui as dpg
from cryptography.fernet import Fernet
from chat_client import ChatClient
from cyphered_gui import *
from generic_callback import GenericCallback



# Taille en octets de la clé
size_key=16


class FernetGUI(CypheredGUI):
    
    def __init__(self) -> None:
        super().__init__()
   
    def run_chat(self, sender, app_data)->None:
        # callback used by the connection windows to start a chat session
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password") 
	
	
        # hashagage des données avec la méthode SHA256 du mot de passe
        # encodage utf-8 
        self._key=hashlib.sha256()
        
        self._key.update(password.encode("utf-8"))
        
        self._key = base64.b64encode(self._key.digest())

        self._log.info(f"Connecting {name}@{host}:{port}")
        self._callback = GenericCallback()
        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    def encrypt(self,message)->bytes:
        # Créer un objet Fernet en utilisant la clé de chiffrement
        fernet=Fernet(self._key)

        # chiffrement à part de la méthode fernet
        encrypted=fernet.encrypt(bytes(message,'utf-8'))

	# Enregistrer un message de log pour le message chiffré
        self._log.info(f"Voci le message chiffré : {bytes_message}")        

        return (encrypted)
        
    def decrypt(self, message_data) -> str:
        encrypted = message_data['data']

	
        encrypted=base64.b64decode(encrypted)
        fernet=Fernet(self._key)


        message_decrypted=fernet.decrypt(message_data)

        return message_decrypted.decode('utf-8')
    
   

if __name__=="__main__":

    logging.basicConfig(level=logging.DEBUG)
    
    client_secured=FernetGUI()
    client_secured.create()
    client_secured.loop()
        