## Prise en main

#Q1 : C'est une topologie client-serveur, nous avons deux clients qui sont connect�s � un serveur

#Q2 : Nous pouvons visualiser les diff�rentes actions effectu�es par le serveur et les clients. Nous pouvons alors visualiser les messages envoy�s entre les deux clients. 

#Q3 : Cela est un probl�me car � travers le serveur, nous avons acc�s � toute la conversation des clients. C'est un probl�me de confidentialit�.

#Q4 : On peut utiliser un algorithme de chiffrement comme l'AES pour chiffrer les messages. Alors, la cl� sym�trique est encod�e avec la cl� publique du destinataire. Les deux donn�es cod�es sont ensuite envoy�es. Une fois re�u, le destinataire utilise sa cl� priv�e pour r�cup�rer la cl� sym�trique d�cod�e et lire le contenu du message.

## Chiffrement

#Q1 : Non ce n'est pas un bon choix, car ce n'est pas r�ellement al�atoire, derri�re il y a un algorithme permettant de simuler l'al�atoire. Donc cette algorithme devient une faille car il est pr�dictif.

#Q2 : Lorsqu'on fait appel � des primitives cryptographiques, une compr�hension compl�te de leur fonctionnement est tr�s important pour identifier et rectifier d'�ventuelles failles. Sans cette compr�hension compl�te, on s'expose � que notre impl�mentation  ai des risques de s�curit�.

#Q3 : Meme si les donn�es soient chiffr�s, une personne mal intentionn�e pourrait toujours interf�rer avec le syst�me en injectant des donn�es incorrectes ou en sur-sollicitant le serveur. Donc le chiffrement n'assure pas toujours une protection compl�te du syst�me.

#Q4 : La propri�t� qui manque ici serait la v�rification d'authentification � l'aide d'HMAC.

## Authenticated Symetric Encryption

#Q1 : Si nous choississons Fernet c'est avantageux compar� aux primitives cryptographiques classiques car sa conception repose sur une fondation bien �tablie, et il g�re de fa�on autonome les complications li�es au padding. De plus, il g�n�re de lui-m�me la cl� secr�te, minimisant ainsi le danger d'une cl� mal choisie ou facilement devinable.

#Q2 : Une technique d'attaque courante est la "retransmission malveillante" ("replay attack" en anglais). Elle vise � intercepter puis r��mettre des messages ant�rieurs dans le but de duper le r�cepteur.

#Q3 : Pour se proteger, on pourrait envisager de mettre un identifiant diff�rents � chaque envoi de message, cela s'appelle timestamp unique � chaque message ou nonce. Ces m�thodes garantissent que chaque message re�u est unique et non un message qui a peut �tre �t� intercepter puis nous a �t� envoy�.

## TTL

#Q1 : L'unique diff�rence que je peux voir est le horodatage, cela permet de pas r�cuperer un message trop vieux car il va g�n�rer une erreur.

#Q2 : On va obtenir erreur car le message sera trop long, c'est pourquoi dans notre code nous avons mit une exception. C'est exactement ce que nous parlions la question pr�c�dente, le message aura d�pass� sa dur�e de vie.

#Q3 : Cette m�thode peut aider � se pr�venir en cas de probl�me avec le serveur mais ne prot�ge pas contre lattaque clairement.

#Q4 : Cette solution pr�sente certaines contraintes, comme les �ventuelles d�calages horaires entre les diff�rents syst�mes, le risque d'attaques par r�utilisation de messages ant�rieurs toujours valides, et l'obligation de conserver un registre des num�ros de s�quence ou des dates pour chaque communication.

#Regard critique

La biblioth�que Fernet, utilis�e pour le chiffrement des communications, a ses faiblesses. Par exemple, elle est inadapt�e au chiffrement de messages de grande taille et g�n�re les iv via une fonction pseudo-al�atoire, ce qui peut les rendre anticipables.

Malgr� le fait que les contenus des messages soient crypt�s et donc ind�chiffrables pour le serveur, les identit�s des destinataires demeurent visibles. Cela permet d'identifier les interactions entre les diff�rents utilisateurs.