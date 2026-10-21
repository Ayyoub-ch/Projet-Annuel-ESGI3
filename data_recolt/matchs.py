# ================================
# IMPORT DES BIBLIOTHÈQUES
# ================================
import requests    # Pour récupérer les données depuis l'API
import os          # Pour créer des dossiers et gérer les fichiers
import json        # Pour manipuler et sauvegarder les fichiers JSON

# ================================
# CONFIGURATION DES DOSSIERS
# ================================

# Dossier principal
DOSSIER_PRINCIPAL = "data_recolt/matchs_data"

# ================================
# DIFFERENTES POSSIBILITES DE MATCH (PASSE, EN COURS, A VENIR)
# ================================


time = ["upcoming","running","past"]

for moment in time:
# ================================
# URL DE L'API JSON
# ================================

    url_api= "https://api.pandascore.co/matches/{moment}?per_page=100&token=SOjDY71vGefSCHtKOX5V3xublQ_W7Hh5ji4LW5TtJ1mhdogtJjg"

# ================================
# RÉCUPÉRATION DES DONNÉES
# ================================

    try:
        response = requests.get(url_api, timeout=600)
        response.raise_for_status()  # Lève une erreur si problème réseau
        
        # Conversion de la réponse en JSON Python
        reponse_json = response.json()
        matchs = reponse_json  # Récupère la liste des leagues
        print(f" {len(matchs)} ligues recuperes depuis l'API")
        
    except requests.exceptions.RequestException as e:
        print(f" Erreur lors de la recuperation des donnees depuis l'API: {e}")
        exit(1)  # Quitte le script avec un code d'erreur
    
# ================================
# TRAITEMENT DE CHAQUE LIGUE
# ================================ 

    for match in matchs:
        try:
            # Extraction des informations de la league
            id= match.get("id")
            nom= match.get("name", "Nom inconnu").replace("/", "_").replace(":", "_").replace(" ", "_")
            jeu= match.get("videogame", {}).get("name", "Jeu inconnu").replace(":", "")
            version = match.get("videogame_version","Aucune version disponible")
            
            date_debut = match.get("begin_at", "Date de début inconnue")[0:10]
            heure_debut = match.get("begin_at", "Heure de début inconnue")[11:19]
            
            date_fin = match.get("end_at", "Date de fin inconnue")[0:10]
            heure_fin = match.get("end_at", "Heure de fin inconnue")[11:19]
            
            
            date_modif = match.get("modified_at", "Date et Heure inconnue")[0:10]
            heure_modif = match.get("modified_at", "Date et Heure inconnue")[11:19]
            
            statut = match.get("status","Aucun statut disponible")
            
            nb_games = match.get("number_of_games","Aucun statut disponible")
            stats_detail = match.get("detailed_stats","Aucun stat disponible")
            
            # Données Live
            live = match.get("live","pas de données pour le live")
            support = live.get("supported")
            
            date_ouverture = live.get("opens_at", "Date inconnue")[0:10]
            heure_ouverture = live.get("opens_at", "Heure inconnue")[11:19]
            
            
            infos_streams = [match.get("streams_list", [{}])[0]] if match.get("streams_list") else [{}]  # Récupère le premier élément de la liste ou un dictionnaire vide si la liste est vide
            main= infos_streams[0].get("main")
            language= infos_streams[0].get("language")
            url= infos_streams[0].get("raw_url")
            
            # Games
            game = match.get("games") or []
            
            # Tournois
            
            
            # Ligue 
           
            # Serie
            
            
            # Création du dossier de la league
            dossier_league = os.path.join(DOSSIER_PRINCIPAL, f"{moment}", f"{jeu}", f"{nom}")
            os.makedirs(dossier_league, exist_ok=True)
            
            # Chemin complet du fichier JSON pour la league
            chemin_fichier_json = os.path.join(dossier_league, f"{id}.json")
            
            
            # Metadonnées et informations de la league
            metadata= {
                "DONNEES GENERALES DE LA LIGUEU MATCH": {
                    "ID": id,
                    "NOM": nom,
                    "JEU VIDEO": jeu,
                    "VERSION ACTUELLE DU JEU": version_actuelle,
                    "DATE DE LA DERNIERE MODIFICATION": date_modif,
                    "HEURE DE LA DERNIERE MODIFICATION": heure_modif,
                },
                "SERIE": {
                    "ID": id_serie,
                    "NOM": full_name_serie if name_serie == "" else name_serie,
                    "ANNEE": annee_serie,
                    "DATE DE DEBUT": date_debut,
                    "HEURE DE DEBUT": heure_debut,
                    "DATE DE FIN": date_fin,
                    "HEURE DE FIN": heure_fin
                }
            }
            
            # Sauvegarde des données dans un fichier JSON
            with open(chemin_fichier_json, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            print(f" Fichier cree '{nom}' sauvegardees dans '{chemin_fichier_json}'")
        
        except Exception as e:
            print(f" Erreur lors du traitement de la league '{nom}': {e}")