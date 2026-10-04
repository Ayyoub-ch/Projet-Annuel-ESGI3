# Projet Annuel ESGI 3

# Thème au choix: E-Sport / Jeux Vidéos / Sports / Ilévia 

## Participants:
- Ayyoub
- Benoit
-Abdelmalek

## But: Développper et Déployer une Plateforme d'OpenData qui traite et affiche des données en tant réel

## Déroulement

1. Recherche d'API Rest (Partie Data) : 
But: Chercher, Comparer et Choisir l'APi correspondante aux données voulues,
l'idéal serait de trouver une API Rest qui donne des accès un minimum gratuit et sans trop de restrictions

2. Extraction / Traitement des données (Partie Data) : 
But: Ecrire le script Python (avec l'aide de Pandas et Numpy) pour nettoyer le fichier de données JSON de l'API, ou le convertir et le rendre plus propre en fonction du format par exemple enlever les lignes vides, adapter ou traiter les caractères génânts.

3. Création de l'API et gestion des routes via FastAPI (Partie AL) : 
But: Créer une API via FastAPI. Il faudra créer des routes (URL sécurisées) menant aux données. L'objectif est que le script écrit à la phase 2 envoit les données 
nettoyées à l'API correspondante, mais également par la suite l'interface Streamlit 
utilisera l'API pour afficher les données en question. L'objectif est de faire une passerelle entre les données et l'interface

3,5. Stockage dans une BDD ou un JSON ? (Partie AL): 
But: Créer et utiliser soit une base de données qui stockera les données de manière permanente ou bien un json qui se mettra à jour continuellement. Dans tous les cas l'API aura pour rôle de communiquer les données issues du Json ou de la BDD. Pour la BDD, c'est au choix entre Mysql ou Postgres

4. Affichage via Streamlit (Partie Data): 
But: Créer une interface Streamlit permettant d'afficher à la manière d'une page web, les données réçues par l'API, on mettra des graphiques et tout autre représentation pour les statistiques et données. Streamlit pourra faire une requête à l'API directement pour avoir accès aux données de l'API de FastAPi

5. Docker (Partie AL)
But: Industrialiser le tout. Cela passe par la création de plusieurs Dockerfile (un pour la BDD, un pour l'API et un autre pour Streamlit) et du fichier docker-compose.yml pour encapsuler : la base de données, l'API FastAPI, et le dashboard Streamlit. L'objectif sera de pouvoir lancer proprement le projet en une seule commande. Cela permettra de garder les dépendances, installations  et la stabilité du projet


# Remarques: 
- Il se peut qu'il y ait des changements en route, mais si vous êtes d'accord pour ce projet dîtes le. Ici j'ai surtout dit le déroulement, le thème est au choix 
- Si vous n'êtes pas d'accord avec quelque chose dîtes le directement

# Points Importants:
- La répartition des tâches seront importantes
- Si quelqu'un galère sur une partie, on essaie de l'aider du mieux que l'on peut
- Utiliser l'IA intelligemment, tant que vous arrivez à comprendre ce qu'il vous sort
- Chercher une alternance assez vite pour qu'on s'en sort 
- ET SURTOUT si par malheur on doit quitter l'école, on doit aider les personnes ayant réussi à trouver une alternance dans le groupe, afin de ne pas lui plomber la fin de son année