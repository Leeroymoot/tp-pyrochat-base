## Prise en main

#Q1 : C'est une topologie client-serveur, nous avons deux clients qui sont connectés à un serveur

#Q2 : Nous pouvons visualiser les différentes actions effectuées par le serveur et les clients. Nous pouvons alors visualiser les messages envoyés entre les deux clients. 

#Q3 : Cela est un problème car à travers le serveur, nous avons accès à toute la conversation des clients. C'est un problème de confidentialité.

#Q4 : On peut utiliser un algorithme de chiffrement comme l'AES pour chiffrer les messages. Alors, la clé symétrique est encodée avec la clé publique du destinataire. Les deux données codées sont ensuite envoyées. Une fois reçu, le destinataire utilise sa clé privée pour récupérer la clé symétrique décodée et lire le contenu du message.

## Chiffrement

#Q1 : Non ce n'est pas un bon choix, car ce n'est pas réellement aléatoire, derrière il y a un algorithme permettant de simuler l'aléatoire. Donc cette algorithme devient une faille car il est prédictif.

#Q2 : Lorsqu'on fait appel à des primitives cryptographiques, une compréhension complète de leur fonctionnement est très important pour identifier et rectifier d'éventuelles failles. Sans cette compr�hension complète, on s'expose à que notre implémentation  ai des risques de sécurité.

#Q3 : Meme si les données soient chiffrés, une personne mal intentionnée pourrait toujours interférer avec le système en injectant des données incorrectes ou en sur-sollicitant le serveur. Donc le chiffrement n'assure pas toujours une protection complète du système.

#Q4 : La propriété qui manque ici serait la vérification d'authentification à l'aide d'HMAC.

## Authenticated Symetric Encryption

#Q1 : Si nous choississons Fernet c'est avantageux comparé aux primitives cryptographiques classiques car sa conception repose sur une fondation bien établie, et il gère de façon autonome les complications liées au padding. De plus, il génère de lui-même la clé secrète, minimisant ainsi le danger d'une clé mal choisie ou facilement devinable.

#Q2 : Une technique d'attaque courante est la "retransmission malveillante" ("replay attack" en anglais). Elle vise à intercepter puis réémettre des messages antérieurs dans le but de duper le récepteur.

#Q3 : Pour se proteger, on pourrait envisager de mettre un identifiant différents à chaque envoi de message, cela s'appelle timestamp unique à chaque message ou nonce. Ces méthodes garantissent que chaque message reçu est unique et non un message qui a peut être été intercepter puis nous a été envoyé.

## TTL

#Q1 : L'unique différence que je peux voir est le horodatage, cela permet de pas r�cuperer un message trop vieux car il va générer une erreur.

#Q2 : On va obtenir erreur car le message sera trop long, c'est pourquoi dans notre code nous avons mit une exception. C'est exactement ce que nous parlions la question précédente, le message aura dépassé sa durée de vie.

#Q3 : Cette méthode peut aider à se prévenir en cas de problème avec le serveur mais ne protége pas contre lattaque clairement.

#Q4 : Cette solution présente certaines contraintes, comme les éventuelles décalages horaires entre les différents systèmes, le risque d'attaques par réutilisation de messages antérieurs toujours valides, et l'obligation de conserver un registre des numéros de séquence ou des dates pour chaque communication.

#Regard critique

La bibliothèque Fernet, utilisée pour le chiffrement des communications, a ses faiblesses. Par exemple, elle est inadaptée au chiffrement de messages de grande taille et génére les iv via une fonction pseudo-aléatoire, ce qui peut les rendre anticipables.

Malgré le fait que les contenus des messages soient cryptés et donc indéchiffrables pour le serveur, les identités des destinataires demeurent visibles. Cela permet d'identifier les interactions entre les différents utilisateurs.