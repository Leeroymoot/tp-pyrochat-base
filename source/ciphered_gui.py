import logging
import base64
import dearpygui.dearpygui as dpg
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from chat_client import ChatClient
from generic_callback import GenericCallback
from basic_gui import *
import os




# Taille en bits d'un bloc de chiffrement
size_block = 128 
# Sel utilisé pour la dérivation de la clé
salt = b"Je_ne_sais_pas"
# Nombre d'itérations pour la dérivation de la clé
nb_itr = 10000
# Taille en octets de la clé
size_key = 16 


class CipheredGUI(BasicGUI):

    #Surcharge du constructeur afin d'ajouter le champ self._key qui contiendra la clef de chiffrement (par default : None)
    def __init__(self) -> None:
        super().__init__() # surcharge du constructeur
        self._client = None
        self._callback = None
        self._log = logging.getLogger(self.__class__.__name__)
        self._key = None 

    #Surcharge de la fonction _create_connection_window() afin d'ajouter un champ password
    def _create_connection_window(self) -> None:
        with dpg.window(label="Connection", pos=(200, 150), width=400, height=300, show=False, tag="connection_windows"):
           
            for field in ["host", "port", "name"]:
                with dpg.group(horizontal=True):
                    dpg.add_text(field)
                    dpg.add_input_text(
                        default_value=DEFAULT_VALUES[field], tag=f"connection_{field}")
            # Ajouter un champ mot de passe
            with dpg.group(horizontal=True):
                dpg.add_text("mot_de_passe")
                dpg.add_input_text(
                    default_value="", tag=f"connection_password", mot_de_passe=True)
               
            dpg.add_button(label="Connect", callback=self.run_chat)


   
    #Surcharger la fonction run_chat() afin d'ajouter la récupération du password et faire la dérivation de clef (self._key)
    def run_chat(self, sender, app_data)->None:
    # callback used by the connection windows to start a chat session    
        host = dpg.get_value("connection_host")
        port = int(dpg.get_value("connection_port"))
        name = dpg.get_value("connection_name")
        password = dpg.get_value("connection_password")
        self._log.info(f"Connecting {name}@{host}:{port}")

        self._callback = GenericCallback()

        self._client = ChatClient(host, port)
        self._client.start(self._callback)
        self._client.register(name)

        # Dérivation de clé
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=size_key,
            salt=salt,
            iterations=nb_itr,
            backend=default_backend()
        )
   
        # Dérivation de la clé en utilisant le mot de passe
        clef = kdf.derive(bytes(password, "utf8"))
        # Stocker la clé dérivée
        self._key = clef

        dpg.hide_item("connection_windows")
        dpg.show_item("chat_windows")
        dpg.set_value("screen", "Connecting")

    def encrypt(self, text):
        # Création d'un vecteur d'initialisation (VI) aléatoire
        initial_vector = os.urandom(16)
       
        # Mise en place du mécanisme de chiffrement avec AES et le mode CTR
        encryption_scheme = Cipher(algorithms.AES(self._key), modes.CTR(initial_vector))
       
        # Création de l'outil de chiffrement à partir du schéma
        message_encoder = encryption_scheme.encryptor()

        # Padding du texte pour assurer la bonne taille
        text_padder = padding.PKCS7(128).padder()
        padded_input = text_padder.update(bytes(text, "utf8")) + text_padder.finalize()

        # Chiffrement du texte
        encoded_output = message_encoder.update(padded_input) + message_encoder.finalize()

        # Renvoyer le vecteur d'initialisation et le texte chiffré
        return (init_vector, encoded_output)
       
 
    def decrypt(self, data):
        #conversion du vecteur d'initialisation et du message :
        iv = base64.b64decode(data[0]["data"])
        encrypted_message = base64.b64decode(data[1]["data"])        

        #déchiffrement du message
        cipher = Cipher(algorithms.AES(self._key), modes.CTR(iv), backend = default_backend())
        decryptor = cipher.decryptor()
        decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()

        #unpadding du message
        unpadder = padding.PKCS7(size_block).unpadder()
        unpadded_message = unpadder.update(decrypted_message) + unpadder.finalize()
        message = str(unpadded_message, "utf-8")

    def recv(self) -> None:
        # Fonction appelée pour recevoir les messages entrants et les afficher
        if self._callback is not None:
            for user, message in self._callback.get():
                decrypted_message = self.decrypt(message) # Déchiffrement du message reçu
                self.update_text_screen(f"{user} : {message}")
            self._callback.clear()

    def send(self, text: str) -> None:
        # Méthode pour transmettre un message
        encrypted_message = self.encrypt(message) # Chiffrement du message à envoyer
        self._client.send_message(encrypted_message)
       


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    # instanciate the class, create context and related stuff, run the main loop
    client = CipheredGUI()
    client.create()
    client.loop()
