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
DOSSIER_PRINCIPAL = "data_recolt/tournaments_data"



# ================================
# URL DE L'API JSON
# ================================

url_api= "https://api.pandascore.co/tournaments?per_page=100&token=SOjDY71vGefSCHtKOX5V3xublQ_W7Hh5ji4LW5TtJ1mhdogtJjg"

# ================================
# RÉCUPÉRATION DES DONNÉES
# ================================

try:
    response = requests.get(url_api, timeout=600)
    response.raise_for_status()  # Lève une erreur si problème réseau
    
    # Conversion de la réponse en JSON Python
    reponse_json = response.json()
    tournaments = reponse_json  # Récupère la liste des tournois
    print(f" {len(tournaments)} tournois recuperes depuis l'API")
    
except requests.exceptions.RequestException as e:
    print(f" Erreur lors de la recuperation des donnees depuis l'API: {e}")
    exit(1)  # Quitte le script avec un code d'erreur
    
# ================================
# TRAITEMENT DE CHAQUE TOURNOI
# ================================ 

for tournament in tournaments:
    try:
        # Extraction des informations du tournoi
        id= tournament.get("id")
        nom= tournament.get("name", "Nom inconnu").replace("/", "_").replace(":", "_").replace(" ", "_").replace(" ", "_").replace("'", "_").replace('"', "_").replace("?", "_").replace("*", "_").replace("<", "_").replace(">", "_").replace("|", "_").replace("#", "_")
        nom_complet= tournament.get("full_name", "Nom complet inconnu").replace("/", "_").replace(":", "_").replace(" ", "_").replace("'", "_").replace('"', "_").replace("?", "_").replace("*", "_").replace("<", "_").replace(">", "_").replace("|", "_").replace("#", "_")
        jeu= tournament.get("videogame", {}).get("name", "Jeu inconnu")
        titre_jeu= (tournament.get("videogame_title") or {}).get("name", "Titre du jeu inconnu") 
        # Le titre du jeu étant un dictionnaire, si ce dernier est juste Nul et que ce n'est même plus un dictionnaire, on met "Titre du jeu inconnu" par défaut en précisant 
        # que cela doit se faire dans le cas où la valeur est nulle.
        
        year= tournament.get("year", "Année inconnue")
        
        date_debut = tournament.get("begin_at", "Date et Heure inconnue")[0:10]
        heure_debut = tournament.get("begin_at", "Date et Heure inconnue")[11:19]
        
        date_fin = tournament.get("end_at", "Date et Heure inconnue")[0:10]
        heure_fin = tournament.get("end_at", "Date et Heure inconnue")[11:19]
        
        date_modif = tournament.get("modified_at", "Date et Heure inconnue")[0:10]
        heure_modif = tournament.get("modified_at", "Date et Heure inconnue")[11:19]
        saison = tournament.get("season", "Saison inconnue")
        

        # Les tournois peuvent être reçus sous forme d'un dictionnaire ou d'une liste.
        matches = tournament.get("matches") or []
        if isinstance(matches, dict):
            matches = [matches]

        matches_metadata = []
        for match in matches:
            if not isinstance(match, dict):
                continue

            modified_at = match.get("modified_at") or "Date inconnue"
            begin_at = match.get("begin_at") or "Date inconnue"
            end_at = match.get("end_at") or "Date inconnue"

            matches_metadata.append({
                "NOM": match.get("name", "Nom de match inconnu"),
                "TYPE": match.get("type", "Type de match inconnu"),
                "PAYS": match.get("country", "Pays du match inconnu") if match.get("country") else "Pays du match inconnu",
                "REGION": match.get("region", "Région du match inconnue") if match.get("region") else "Région du match inconnue",
                "DATE DE DEBUT": begin_at[0:10],
                "HEURE DE DEBUT": begin_at[11:19],
                "DATE DE FIN": end_at[0:10],
                "HEURE DE FIN": end_at[11:19],
                "DATE DE LA DERNIERE MODIFICATION": modified_at[0:10],
                "HEURE DE LA DERNIERE MODIFICATION": modified_at[11:19],
                "PRIZEPOOL": tournament.get("prizepool", "Prizepool du tournoi inconnu") if tournament.get("prizepool", "Prizepool du tournoi inconnu") else "Prizepool du tournoi inconnu",
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
        
        # Chemin complet du fichier JSON pour la serie
        chemin_fichier_json = os.path.join(dossier_serie, f"{nom}.json")
        
        
        # Metadonnées et informations de la serie
        metadata= {
             "DONNEES GENERALES DE LA SERIE": {
                "ID": id,
                "NOM": nom_complet if nom == "" else nom,
                "JEU VIDEO": jeu if jeu != None and jeu != "" else titre_jeu if titre_jeu != None and titre_jeu != "" else "Jeu vidéo inconnu",
                "DATE DE DEBUT": date_debut,
                "HEURE DE DEBUT": heure_debut,
                "DATE DE FIN": date_fin,
                "HEURE DE FIN": heure_fin,
                "DATE DE LA DERNIERE MODIFICATION": date_modif,
                "HEURE DE LA DERNIERE MODIFICATION": heure_modif,
                "ANNEE": "Année inconnue" if year == "" or year == "null" else year,
                "SAISON": "Saison inconnue" if saison == "" or saison == "null" else saison,
             },
             "MATCHES": matches_metadata
        }
    
        
        # Sauvegarde des données dans un fichier JSON
        with open(chemin_fichier_json, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=4)
        print(f" Fichier cree '{nom_complet}' sauvegardees dans '{chemin_fichier_json}'")
    
    except Exception as e:
        print(f" Erreur lors du traitement du tournoi '{nom}': {e}")