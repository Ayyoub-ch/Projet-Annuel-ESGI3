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
DOSSIER_PRINCIPAL = "data_recolt/series_data"



# ================================
# URL DE L'API JSON
# ================================

url_api= "https://api.pandascore.co/series?token=SOjDY71vGefSCHtKOX5V3xublQ_W7Hh5ji4LW5TtJ1mhdogtJjg"

# ================================
# RÉCUPÉRATION DES DONNÉES
# ================================

try:
    response = requests.get(url_api, timeout=600)
    response.raise_for_status()  # Lève une erreur si problème réseau
    
    # Conversion de la réponse en JSON Python
    reponse_json = response.json()
    series = reponse_json  # Récupère la liste des series
    print(f" {len(series)} series récupérées depuis l'API")
    
except requests.exceptions.RequestException as e:
    print(f" Erreur lors de la récupération des données depuis l'API: {e}")
    exit(1)  # Quitte le script avec un code d'erreur
    
# ================================
# TRAITEMENT DE CHAQUE SÉRIE
# ================================ 

for serie in series:
    try:
        # Extraction des informations de la série
        id= serie.get("id")
        nom= serie.get("name", "Nom inconnu")
        jeu= serie.get("videogame", {}).get("name", "Jeu inconnu")
        version_actuelle = serie.get("current_version", "Version inconnue")
        date_modif = serie.get("modified_at", "Date et Heure inconnue")[0:10]
        heure_modif = serie.get("modified_at", "Date et Heure inconnue")[11:19]

        # Extraction des informations de la série
        for tournament in series.get("tournaments", []):
            tournament_name= tournament.get("name", "Nom de tournoi inconnu")
            tournament_type= tournament.get("type", "Type de tournoi inconnu")
            tournament_country= tournament.get("country", "Pays du tournoi inconnu")
            tournament_region= tournament.get("region", "Région du tournoi inconnue")
            tournament_modified_at= tournament.get("modified_at", "Date et Heure de modification du tournoi inconnue")
            tournament_begin_at = tournament.get("begin_at", "Date et Heure de début du tournoi inconnue")
            tournament_end_at = tournament.get("end_at", "Date et Heure de fin du tournoi inconnue")
            tournament_tier= tournament.get("tier", "Tier du tournoi inconnu")
            tournament_prizepool = tournament.get("prizepool", "Prizepool du tournoi inconnu")
            tournament_detailed_stats= tournament.get("detailed_stats", "Statistiques détaillées du tournoi inconnues")
            tournament_live_supported= tournament.get("live_supported", "Live supporté inconnu")
        
        ## Remarque : Si une partie de l'information n'est pas sous forme de dictionnaire, c'est une liste
        ## Donc on doit faire une boucle for pour récupérer les informations de chaque série. 
        ## Cependant, si la série est vide, on ne fait rien.
        
        # Création du dossier de la league
        dossier_serie = os.path.join(DOSSIER_PRINCIPAL, f"{nom}")
        os.makedirs(dossier_serie, exist_ok=True)
        
        # Chemin complet du fichier JSON pour la league
        chemin_fichier_json = os.path.join(dossier_serie, f"{nom}.json")
        
        
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
             "TOURNOI": {
                 "NOM": tournament_name,
                 "TYPE": tournament_type,
                 "DATE DE DEBUT": tournament_begin_at,
                 "DATE DE FIN": tournament_end_at,
                 "PRIZEPOOL": tournament_prizepool
             }
             }
        }
        
        # Sauvegarde des données dans un fichier JSON
        with open(chemin_fichier_json, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print(f" Fichier créé '{nom}' sauvegardées dans '{chemin_fichier_json}'")
    
    except Exception as e:
        print(f" Erreur lors du traitement de la série '{nom}': {e}")