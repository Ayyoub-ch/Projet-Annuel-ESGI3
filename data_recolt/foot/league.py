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
DOSSIER_PRINCIPAL = "data/football/leagues_data"



# ================================
# URL DE L'API JSON
# ================================

url_api= "https://v3.football.api-sports.io/leagues"

headers = {
    'x-apisports-key': "dc56c5bba70f6f222790a01874888304"
    }

# ================================
# RÉCUPÉRATION DES DONNÉES
# ================================

try:
    response = requests.get(url_api, headers=headers, timeout=600)
    response.raise_for_status()  # Lève une erreur si problème réseau
    
    # Conversion de la réponse en JSON Python
    reponse_json = response.json()
    leagues_data = reponse_json.get("response", [])
    print(f" {len(leagues_data)} ligues récupérées depuis l'API")
    
except requests.exceptions.RequestException as e:
    print(f" Erreur lors de la recuperation des donnees depuis l'API: {e}")
    exit(1)  # Quitte le script avec un code d'erreur
    
# ================================
# TRAITEMENT DE CHAQUE LIGUE
# ================================ 

if not isinstance(leagues_data, list):
    raise ValueError("La propriété 'response' de l'API n'est pas une liste.")

for league_data in leagues_data:
    if not isinstance(league_data, dict):
        print(f"Entrée de ligue ignorée car elle n'est pas un objet : {league_data}")
        continue

    league = league_data.get("league")
    # Si la liste ne contient pas de dictionnaire alors on passe
    if not isinstance(league, dict):
        print(f"Entrée ignorée car elle ne contient pas d'objet 'league' : {league_data}")
        continue

    id_ligue = league.get("id")
    nom_ligue = league.get("name").replace("/", "_").replace(":", "_").replace(" ", "_").replace("\u0131", "i")
    type_ligue = league.get("type")

    if id_ligue is None or not nom_ligue:
        print(f"Ligue ignorée car son ID ou son nom est absent : {league}")
        continue
    
    country = league_data.get("country")
    # Si la liste ne contient pas de dictionnaire alors on passe
    if not isinstance(league, dict):
        print(f"Entrée ignorée car elle ne contient pas d'objet 'league' : {league_data}")
        continue
    nom_pays = country.get("name")
    
    seasons = league_data.get("seasons", [])
    
    if not isinstance(seasons, list):
        raise ValueError("Saisons inexistantes")
    
    saisons = []
    for season in seasons:
        if not isinstance(season, dict):
            print(f"Saison Manquante : {season}")
            continue
        
        
        annee_saison = season.get("year")
        
        date_heure_debut = season.get("begin_at", "Date et Heure de la série inconnue")
        date_debut = date_heure_debut[0:10] if date_heure_debut != "Date et Heure de la série inconnue" else "Date de début de la saison inconnue"
        heure_debut = date_heure_debut[11:19] if date_heure_debut != "Date et Heure de la série inconnue" else "Heure de début de la saison inconnue"
        
        date_heure_fin = season.get("end_at", "Date et Heure de la série inconnue")
        date_fin = date_heure_fin[0:10] if date_heure_fin != "Date et Heure de la série inconnue" else "Date de fin inconnue"
        heure_fin = date_heure_fin[11:19] if date_heure_fin != "Date et Heure de la série inconnue" else "Heure de fin inconnue"
        
        saison_actuelle = season.get("current")
        
        saisons.append({
            "ANNEE": annee_saison,
            "DATE DE DEBUT": date_debut,
            "HEURE DE DEBUT": heure_debut,
            "DATE DE FIN": date_fin,
            "HEURE DE FIN": heure_fin
        })
    
    
    
    

    nom_dossier = nom_ligue.replace("/", "_").replace(":", "_").replace(" ", "_")
    dossier_league = os.path.join(DOSSIER_PRINCIPAL, nom_pays)
    os.makedirs(dossier_league, exist_ok=True)

    chemin_fichier_json = os.path.join(dossier_league, f"{nom_dossier}.json")

    metadata = {
        "DONNEES GENERALES DE LA LIGUE": {
            "ID": id_ligue,
            "NOM": nom_ligue,
            "TYPE": type_ligue
        },
        "SAISONS": saisons
    }

    try:
        with open(chemin_fichier_json, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print(f"Ligue '{nom_ligue}' (ID {id_ligue}) sauvegardée dans '{chemin_fichier_json}'")
    except OSError as e:
        print(f"Erreur lors de la sauvegarde de la ligue '{id_ligue}' : {e}")