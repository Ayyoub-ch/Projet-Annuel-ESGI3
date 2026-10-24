# Projet-Annuel-ESGI3

# Présentation globale du projet
## Contexte :

Dans le cadre de notre formation en 3e Année de Bachelor à l'ESGI de Lille, nous sommes amenés à réaliser un projet par groupe de 3 à 4 personnes. Le thème est au choix.
Le projet sera présenté en classe, le tout avec une soutenance orale.

## But

- Pouvoir travailler en groupe avec des gens ayants plusieurs compétences différentes afin de réaliser un projet complet et pertinent 
- Le jury s'appuiera essentiellement sur la structure du projet et son architecture


# Présentation détaillée du projet
## Thème et Déroulement du projet

Ce projet se porte sur le thème du sport dans sa globalité, cela englobera les sports tradtionnels (football, basketball, rugby) jusqu'aux sports non "conventionnels" comme les échecs ou l'e-sport.
Le projet doit aboutir à une plateforme qui permet de récupérer les données des différents sports, afin que les utilisateurs puissent utiliser, récupérer et explorer les données qui leur conviennent.
Le tout en centralisant les différentes API liées au sport.


On travaille exclusivement avec Python et ses librairies ( FastApi et Streamlit)


##  Partie 1: Récolte, Traitement et Nettoyage des données 

Pour commencer, il faut qu'on sache comment on trouve les données, pour cela on a du chercher des APIS d'Opend Data, soit des Apis donnant l'accès à des données dites libres d'accès, donc non soumis à une réglementation ou à un abonnement à payer pour utiliser ou voir 
les données.

Après avoir choisi et tester l'API via un outil comme Postman, qui permet de lecteut d'url API afin de vérifier et tester si les données sont correctes et comment elles sont structurées. Par ailleurs on regarde aussi via la documentation des APIS, les différents Endpoints
possibles, afin d'avoir accès à différent types de données.

Après avoir vérifié que les données testées sont opérationnelles, on les nettoie et range par dossier et fichier json avec les informations les plus importantes.

On va illustrer avec le cas de  l'e-sport:

On a dans data_recolt, chacun des scripts de traitement pour un endpoint particulier:

/tournament
/serie
/matches
/league

Lors du traitement de chacun on les place en fonction du nom du jeu puis du nom tout court et on met le fichier par id 

Par exemple :

On obtiendra comme chemin suivant après le traitement des données de l'API:

data_recolt\data\tournaments_data\Counter-Strike\Playoffs\22202.json