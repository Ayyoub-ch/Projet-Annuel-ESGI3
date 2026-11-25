
# ================================
# IMPORT DES BIBLIOTHÈQUES
# ================================
import requests    # Pour récupérer les données depuis l'API
import os          # Pour créer des dossiers et gérer les fichiers
import json        # Pour manipuler et sauvegarder les fichiers JSON
import time        # Pour respecter la limite de requêtes de l'API
import sys

sys.stdout.reconfigure(encoding="utf-8")

# ================================
# CONFIGURATION DES DOSSIERS
# ================================





caf_leagues = [1008, 12, 20, 973, 533, 1015, 1164]
seasons = [2022,2023,2024]


# Dossier principal
DOSSIER_PRINCIPAL = "./data/football/fixtures_data"



# ================================
# URL DE L'API JSON
# ================================
c=0
for caf_league in caf_leagues:
    for season in seasons:
        url_api= f"https://v3.football.api-sports.io/fixtures?season={season}&league={caf_league}"
        c+=1
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
        caf_leagues_data = reponse_json.get("response", [])
        print(f" {len(caf_leagues_data)} ligues de la CAF recuperees depuis l'API")

        if c % 10 == 0:
            print("Pause d'une minute pour respecter la limite de l'API.")
            time.sleep(60)
        
    except requests.exceptions.RequestException as e:
        print(f" Erreur lors de la recuperation des donnees depuis l'API: {e}")
        exit(1)  # Quitte le script avec un code d'erreur
        
    # ================================
    # TRAITEMENT DE CHAQUE EQUIPE
    # ================================ 

    if not isinstance(caf_leagues_data, list):
        raise ValueError("La propriété 'response' de l'API n'est pas une liste.")

    for caf_league_data in caf_leagues_data:
        if not isinstance(caf_league_data, dict):
            print(f"Entrée de ligue ignorée car elle n'est pas un objet : {caf_league_data}")
            continue

        fixture = caf_league_data.get("fixture")
        # Si la liste ne contient pas de dictionnaire alors on passe
        if not isinstance(fixture, dict):
            print(f"Entrée ignorée car elle ne contient pas d'objet 'league' : {caf_league_data}")
            continue
        
        id_fixture = fixture.get("id")
        referee_fixture = fixture.get("referee")
        timezone_fixture = fixture.get("timezone")
        date_fixture = fixture.get("date")
        timestamp_fixture = fixture.get("timestamp")
        
        periods_fixture = fixture.get("periods")
        premiere_periode = periods_fixture.get("first")
        seconde_periode = periods_fixture.get("second")
        
        
        stade = caf_league_data.get("venue")
        if not isinstance(stade, dict):
            print(f"Entrée ignorée car elle ne contient pas d'objet 'league' : {caf_league_data}")
            continue
        
        id_stade = stade.get("id")
        nom_stade= stade.get("name")
        adresse_stade = stade.get("address")
        ville_stade = stade.get("city")
        capacite_stade = stade.get("capacity")
        surface_stade = stade.get("surface")
        
        
        nom_dossier = nom_team.replace("/", "_").replace(":", "_").replace(" ", "_")
        dossier_team = os.path.join(DOSSIER_PRINCIPAL, pays_team)
        os.makedirs(dossier_team, exist_ok=True)

        chemin_fichier_json = os.path.join(dossier_team, f"{nom_dossier}.json")

        metadata = {
            "DONNEES GENERALES DE L'EQUIPE'": {
                "ID": id_team,
                "NOM": nom_team,
                "CODE": code_team,
                "PAYS": pays_team,
                "ANNEE FONDATION":annee_fondation_team,
                "NATIONALE": national
            },
            "STADE": {
                "ID": id_stade,
                "NOM": nom_stade,
                "ADRESSE": adresse_stade,
                "VILLE": ville_stade,
                "CAPACITE": capacite_stade,
                "SURFACE": surface_stade
            }
        }

        try:
            with open(chemin_fichier_json, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            print(f"Equipe '{nom_team}' (PAYS {pays_team}) (ID {id_team}) sauvegardée dans '{chemin_fichier_json}'")
        except OSError as e:
            print(f"Erreur lors de la sauvegarde de la ligue '{id_team}' : {e}")




