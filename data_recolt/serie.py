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
        nom_complet= serie.get("full_name", "Nom complet inconnu")
        jeu= serie.get("videogame", {}).get("name", "Jeu inconnu")
        titre_jeu= serie.get("videogame_title", {}).get("name", "Titre du jeu inconnu")
        year= serie.get("year", "Année inconnue")
        
        date_debut = serie.get("begin_at", "Date et Heure inconnue")[0:10]
        heure_debut = serie.get("begin_at", "Date et Heure inconnue")[11:19]
        
        date_fin = serie.get("end_at", "Date et Heure inconnue")[0:10]
        heure_fin = serie.get("end_at", "Date et Heure inconnue")[11:19]
        
        date_modif = serie.get("modified_at", "Date et Heure inconnue")[0:10]
        heure_modif = serie.get("modified_at", "Date et Heure inconnue")[11:19]
        saison = serie.get("season", "Saison inconnue")
        
        # Extraction des informations de la ligue associée à la série
        league = serie.get("league", {})
        league_id = league.get("id", "ID de ligue inconnu")
        league_name = league.get("name", "Nom de ligue inconnu")
        league_country = league.get("country", "Pays de la ligue inconnu")
        league_modified_at_date = league.get("modified_at", "Date et Heure de modification de la ligue inconnue")[0:10]
        league_modified_at_heure = league.get("modified_at", "Date et Heure de modification de la ligue inconnue")[11:19]


        # Les tournois peuvent être reçus sous forme d'un dictionnaire ou d'une liste.
        tournaments = serie.get("tournaments") or []
        if isinstance(tournaments, dict):
            tournaments = [tournaments]

        tournament_metadata = []
        for tournament in tournaments:
            if not isinstance(tournament, dict):
                continue

            modified_at = tournament.get("modified_at") or "Date inconnue"
            begin_at = tournament.get("begin_at") or "Date inconnue"
            end_at = tournament.get("end_at") or "Date inconnue"

            tournament_metadata.append({
                "NOM": tournament.get("name", "Nom de tournoi inconnu"),
                "TYPE": tournament.get("type", "Type de tournoi inconnu"),
                "PAYS": tournament.get("country", "Pays du tournoi inconnu"),
                "REGION": tournament.get("region", "Région du tournoi inconnue"),
                "DATE DE DEBUT": begin_at[0:10],
                "HEURE DE DEBUT": begin_at[11:19],
                "DATE DE FIN": end_at[0:10],
                "HEURE DE FIN": end_at[11:19],
                "DATE DE LA DERNIERE MODIFICATION": modified_at[0:10],
                "HEURE DE LA DERNIERE MODIFICATION": modified_at[11:19],
                "PRIZEPOOL": tournament.get("prizepool", "Prizepool du tournoi inconnu"),
                "SLUG": tournament.get("slug", "Slug du tournoi inconnu"),
                "TIER": tournament.get("tier", "Tier du tournoi inconnu"),
                "STATISTIQUES DETAILLEES": tournament.get(
                    "detailed_stats",
                    "Statistiques détaillées du tournoi inconnues",
                ),
                "LIVE SUPPORTÉ": tournament.get("live_supported", "Live supporté inconnu"),
            })
        
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
             "DONNEES GENERALES DE LA SERIE": {
                "ID": id,
                "NOM": nom,
                "NOM COMPLET": nom_complet,
                "JEU VIDEO": jeu,
                "TITRE DU JEU": titre_jeu,
                "DATE DE DEBUT": date_debut,
                "HEURE DE DEBUT": heure_debut,
                "DATE DE FIN": date_fin,
                "HEURE DE FIN": heure_fin,
                "DATE DE LA DERNIERE MODIFICATION": date_modif,
                "HEURE DE LA DERNIERE MODIFICATION": heure_modif,
                "ANNEE": year,
                "SAISON": saison
             },
             "LIGUE": {
                "ID": league_id,
                "NOM": league_name,
                "PAYS": league_country,
                "DATE DE LA DERNIERE MODIFICATION": league_modified_at_date,
                "HEURE DE LA DERNIERE MODIFICATION": league_modified_at_heure
            },
             "TOURNOIS": tournament_metadata
        }
    
        
        # Sauvegarde des données dans un fichier JSON
        with open(chemin_fichier_json, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print(f" Fichier créé '{nom}' sauvegardées dans '{chemin_fichier_json}'")
    
    except Exception as e:
        print(f" Erreur lors du traitement de la série '{nom}': {e}")