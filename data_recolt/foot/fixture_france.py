
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




france_leagues = [ ]
seasons = [2022,2023,2024]


# Dossier principal
DOSSIER_PRINCIPAL = "./data/football/fixtures_data"



# ================================
# URL DE L'API JSON
# ================================
c=0
for country in countries:
    url_api= f"https://v3.football.api-sports.io/teams?country={country}"
    c+=1

    headers = {
        'x-apisports-key': "dc56c5bba70f6f222790a01874888304"
        }

# ================================
# RÉCUPÉRATION DES DONNÉES
# ================================
    if c ==100:
        break
    try:

        response = requests.get(url_api, headers=headers, timeout=600)
        response.raise_for_status()  # Lève une erreur si problème réseau
        
        # Conversion de la réponse en JSON Python
        reponse_json = response.json()
        teams_data = reponse_json.get("response", [])
        print(f" {len(teams_data)} equipes recuperees depuis l'API")

        if c % 10 == 0:
            print("Pause d'une minute pour respecter la limite de l'API.")
            time.sleep(60)
        
    except requests.exceptions.RequestException as e:
        print(f" Erreur lors de la recuperation des donnees depuis l'API: {e}")
        exit(1)  # Quitte le script avec un code d'erreur
        
    # ================================
    # TRAITEMENT DE CHAQUE EQUIPE
    # ================================ 

    if not isinstance(teams_data, list):
        raise ValueError("La propriété 'response' de l'API n'est pas une liste.")

    for team_data in teams_data:
        if not isinstance(team_data, dict):
            print(f"Entrée de ligue ignorée car elle n'est pas un objet : {team_data}")
            continue

        team = team_data.get("team")
        # Si la liste ne contient pas de dictionnaire alors on passe
        if not isinstance(team, dict):
            print(f"Entrée ignorée car elle ne contient pas d'objet 'league' : {team_data}")
            continue
        
        id_team = team.get("id")
        nom_team = team.get("name").replace("/", "_").replace(":", "_").replace(" ", "_").replace("\u0131", "i")
        code_team = team.get("code","Aucun code")
        pays_team = team.get("country","Pas de pays défini")
        annee_fondation_team = team.get("founded","Aucune année de fondation trouvée")
        national = team.get("national")
        
        
        stade = team_data.get("venue")
        if not isinstance(stade, dict):
            print(f"Entrée ignorée car elle ne contient pas d'objet 'league' : {team_data}")
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




