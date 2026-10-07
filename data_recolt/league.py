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
DOSSIER_PRINCIPAL = "data_recolt/leagues_data"



# ================================
# URL DE L'API JSON
# ================================

url_api= "https://api.pandascore.co/leagues?token=SOjDY71vGefSCHtKOX5V3xublQ_W7Hh5ji4LW5TtJ1mhdogtJjg"

# ================================
# RÉCUPÉRATION DES DONNÉES
# ================================

try:
    response = requests.get(url_api, timeout=600)
    response.raise_for_status()  # Lève une erreur si problème réseau
    
    # Conversion de la réponse en JSON Python
    reponse_json = response.json()
    leagues = reponse_json  # Récupère la liste des leagues
    print(f" {len(leagues)} leagues récupérés depuis l'API")
    
except requests.exceptions.RequestException as e:
    print(f" Erreur lors de la récupération des données depuis l'API: {e}")
    exit(1)  # Quitte le script avec un code d'erreur
    
# ================================
# TRAITEMENT DE CHAQUE LIGUE
# ================================ 

for league in leagues:
    try:
        # Extraction des informations de la league
        id= league.get("id")
        nom= league.get("name", "Nom inconnu")
        jeu= league.get("videogame", {}).get("name", "Jeu inconnu")
        version_actuelle = league.get("current_version", "Version inconnue")
        date = league.get("modified_at", "Date et Heure inconnue")[0:10]
        heure = league.get("modified_at", "Date et Heure inconnue")[11:19]

        # Extraction des informations de la série
        # id_serie= league.get("series", {}).get("id", "ID de série inconnu")
        # name_serie= league.get("series", {}).get("name", "Nom de série inconnu")
        # annee_serie= league.get("series", {}).get("year", "Année de série inconnue")
        
        # date_heure_debut = league.get("series", {}).get("begin_at", "Date et Heure de la série inconnue")
        # date_debut = date_heure_debut[0:10] if date_heure_debut != "Date et Heure de la série inconnue" else "Date de début inconnue"
        # heure_debut = date_heure_debut[11:19] if date_heure_debut != "Date et Heure de la série inconnue" else "Heure de début inconnue"
        
        # date_heure_fin = league.get("series", {}).get("end_at", "Date et Heure de la série inconnue")
        # date_fin = date_heure_fin[0:10] if date_heure_fin != "Date et Heure de la série inconnue" else "Date de fin inconnue"
        # heure_fin = date_heure_fin[11:19] if date_heure_fin != "Date et Heure de la série inconnue" else "Heure de fin inconnue"
        
        # full_name_serie= league.get("series", {}).get("full_name", "Nom complet de série inconnu")
        
        # Création du dossier de la league
        dossier_league = os.path.join(DOSSIER_PRINCIPAL, f"{nom}")
        os.makedirs(dossier_league, exist_ok=True)
        
        # Chemin complet du fichier JSON pour la league
        chemin_fichier_json = os.path.join(dossier_league, f"{nom}.json")
        
        
        # Metadonnées et informations de la league
        metadata= {
             "DONNEES GENERALES DE LA LIGUE": {
                "ID": id,
                "NOM": nom,
                "JEU VIDEO": jeu,
                "VERSION ACTUELLE DU JEU": version_actuelle,
                "DATE": date,
                "HEURE": heure,
             },
            #  "SERIE": {
            #     "ID": id_serie,
            #     "NOM": name_serie,
            #     "ANNEE": annee_serie,
            #     "DATE DE DEBUT": date_debut,
            #     "HEURE DE DEBUT": heure_debut,
            #     "DATE DE FIN": date_fin,
            #     "HEURE DE FIN": heure_fin,
            #     "NOM COMPLET": full_name_serie
            #  }
        }
        
        # Sauvegarde des données dans un fichier JSON
        with open(chemin_fichier_json, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print(f" Fichier créé '{nom}' sauvegardées dans '{chemin_fichier_json}'")
    
    except Exception as e:
        print(f" Erreur lors du traitement de la league '{nom}': {e}")