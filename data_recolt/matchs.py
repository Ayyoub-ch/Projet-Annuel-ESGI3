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
DOSSIER_PRINCIPAL = "data_recolt/data/matchs_data"

# ================================
# DIFFERENTES POSSIBILITES DE MATCH (PASSE, EN COURS, A VENIR)
# ================================


time = ["upcoming","running","past"]

for moment in time:
# ================================
# URL DE L'API JSON
# ================================

    url_api= f"https://api.pandascore.co/matches/{moment}?per_page=100&token=SOjDY71vGefSCHtKOX5V3xublQ_W7Hh5ji4LW5TtJ1mhdogtJjg"
    print("\n", "Dossier :", moment, "\n")

# ================================
# RÉCUPÉRATION DES DONNÉES
# ================================

    try:
        response = requests.get(url_api, timeout=600)
        response.raise_for_status()  # Lève une erreur si problème réseau
        
        # Conversion de la réponse en JSON Python
        reponse_json = response.json()
        matchs = reponse_json  # Récupère la liste des leagues
        print(f" {len(matchs)} matchs recuperes depuis l'API")
        
    except requests.exceptions.RequestException as e:
        print(f" Erreur lors de la recuperation des donnees depuis l'API: {e}")
        exit(1)  # Quitte le script avec un code d'erreur
    
# ================================
# TRAITEMENT DE CHAQUE LIGUE
# ================================ 

    for match in matchs:
        try:
            # Extraction des informations de la league
            id= match.get("id","Id inconnu")
            nom= match.get("name", "Nom inconnu").replace("/", "_").replace(":", "_").replace(" ", "_")
            type = match.get("match_type","Aucun type de match")
            jeu= match.get("videogame", {}).get("name", "Jeu inconnu").replace(":", "").replace("-", " ")
            version = match.get("videogame_version","Aucune version disponible") if match.get("videogame_version","Aucune version disponible") != None else "Version indisponible"
            
            debut_match = match.get("begin_at")
            if debut_match != None:
                date_debut = debut_match[0:10]
                heure_debut = debut_match[11:19]
            else:
                debut_match = "Aucune information sur le début du match"
                
            match_fin = match.get("end_at")
            date_fin = match_fin[0:10] if match_fin else "Date de fin non définie"
            heure_fin = match_fin[11:19] if match_fin else "Heure de fin non définie"
            
            date_modif = match.get("modified_at", "Date de modification inconnue")[0:10]
            heure_modif = match.get("modified_at", "Date de modification inconnue")[11:19]
            
            statut = match.get("status","Aucun statut disponible")
            
            nb_games = match.get("number_of_games","Nombre de game indisponible")
            stats_detail = match.get("detailed_stats","Aucun stat détaillée disponible")
            
            # Données Live
            live = match.get("live","pas de données pour le live")
            support = live.get("supported","Pas supporte")
            
            ouverture =  live.get("opens_at")
            if ouverture != None :
                date_ouverture = ouverture[0:10]
                heure_ouverture = ouverture[11:19]
            else:
                ouverture = "Pas d'information sur l'ouverture"
            
            avantage_partie = match.get("game_advantage","Pas d'avantage particulier") if match.get("game_advantage","Pas d'avantage particulier") != None else "Pas d'avantage lors de la partie"
            
            # Games
            games = match.get("games") or []
            if isinstance(games,dict):
                games = [games]
            
            parties = []
            
            if not games :
                parties = "Pas d'informations sur les parties"
            else:
                for game in games:
                    if not isinstance(game,dict):
                        continue
                    
                    id_partie = game.get("id", "Date de début inconnue")
                    partie_fini = game.get("complete", "Pas d'info sur la finition de la partie")
                    position_partie = game.get("position", "Pas d'info sur la position de la partie")
                    statut_partie = game.get("status", "Pas de statut disponible")
                    longueur_partie = game.get("length", "Pas de longueur disponible") if game.get("length", "Pas de longueur disponible") != None else "Pas de longueur disponible"
                    
                    debut_partie = game.get("begin_at")
                    date_debut_partie = debut_partie[0:10] if debut_partie else "Date de début de partie non définie"
                    heure_debut_partie = debut_partie[11:19] if debut_partie else "Heure de début de partie non définie"
                    
                        
                    fin_partie = game.get("end_at")
                    date_fin_partie = fin_partie[0:10] if fin_partie else "Date de fin de partie non définie"
                    heure_fin_partie = fin_partie[11:19] if fin_partie else "Heure de fin de partie non définie"
                    
                    stats_detail = game.get("detailed_stats", "Date de début inconnue")
                    forfait = game.get("forfeit", "Date de début inconnue")
                    
                    vainqueur = game.get("winner") or {}
                    vainqueur_id = vainqueur.get("id","Id vainqueur non disponible") if vainqueur.get("id","Id vainqueur non disponible") != None else "Pas de Vainqueur disponible"
                    vainqueur_type = vainqueur.get("type", "Type de vainqueur inconnu")
                    winner_type = game.get("winner_type", "Type de vainqueur inconnu")
                    
                    parties.append({
                        "ID": id_partie,
                        "PARTIE FINIE": partie_fini,
                        "POSITION PARTIE": position_partie,
                        "STATUT": statut_partie,
                        "LONGUEUR": longueur_partie,
                        "DATE DE DEBUT DE PARTIE": date_debut_partie,
                        "HEURE DE DEBUT DE PARTIE": heure_debut_partie,
                        "DATE DE FIN DE PARTIE": date_fin_partie,
                        "HEURE DE FIN DE PARTIE": heure_fin_partie,
                        "DETAIL STAT": stats_detail,
                        "FORFAIT": forfait,
                        
                        "VAINQUEUR" :{
                            "ID": vainqueur_id,
                            "TYPE": vainqueur_type
                        },
                        "TYPE DU VAINQUEUR": winner_type
                    })
                    
            # Infos Stream
            infos_streams = [match.get("streams_list", [{}])[0]] if match.get("streams_list") else [{}]  # Récupère le premier élément de la liste ou un dictionnaire vide si la liste est vide
            main= infos_streams[0].get("main","Aucune info principale")
            language= infos_streams[0].get("language","Pas de langue définie")
            url= infos_streams[0].get("raw_url","Pas d'information sur l'url ")   
            
            # Tournois
            tournois = match.get("tournament")
            id_tournoi = tournois.get("id","Id inconnu")
            nom_tournoi = tournois.get("name", "Nom incconu")
            type_tournoi = tournois.get("type","Type inconnu")
            pays_tournoi = tournois.get("country","Pays inconnu")
            region_tournoi = tournois.get("region","Region inconnu")
            tier_tournoi = tournois.get("tier","Tier inconnu")
            cash_prize_tournoi = tournois.get("prizepool","Cash Prize inconnu")
            winner_tournoi = tournois.get("winner_id","Vainqueur inconnu") if tournois.get("winner_id","Vainqueur inconnu") else "Pas d'information sur le vainqueur du tournoi"
            stat_detail_tournoi = tournois.get("detailed_stats","Stats detaillees inconnues")
            live_supported_tournoi = tournois.get("live_supported", "Live supporte inconnu")
            date_debut_tournoi = tournois.get("begin_at", "Date de début inconnue")[0:10]
            heure_debut_tournoi = tournois.get("begin_at", "Heure de début inconnue")[11:19]              
            date_fin_tournoi = tournois.get("end_at", "Date de début inconnue")[0:10]
            heure_fin_tournoi = tournois.get("end_at", "Heure de début inconnue")[11:19]
            date_modif_tournoi = tournois.get("modified_at", "Date de modification inconnue")[0:10]
            heure_modif_tournoi = tournois.get("modified_at", "Heure de modification inconnue")[11:19]

            
            # Ligue 
            ligues = match.get("league")
            id_ligue = ligues.get("id","Id indisponible")
            nom_ligue = ligues.get("name","Nom indisponible")
            date_modif_ligue = ligues.get("modified_at", "Date de modification inconnue")[0:10]
            heure_modif_ligue = ligues.get("modified_at", "Heure de modification inconnue")[11:19]   
           
            # Serie
            series = match.get("serie")
            id_serie = series.get("id","Id inconnu")
            nom_serie = series.get("full_name", "Nom incconu")
            annee_serie = series.get("year","Annee inconnue")
            saison_serie = series.get("season","Saison Inconnue") if series.get("season","Saison Inconnue") != None else "Saison inconnue"
            winner_serie = series.get("winner_id","Vainqueur inconnu") if series.get("winner_id","Vainqueur inconnu") != None else "Vainqueur iconnu"
            date_debut_serie = series.get("begin_at", "Date de début inconnue")[0:10]
            heure_debut_serie = series.get("begin_at", "Heure de début inconnue")[11:19]              
            date_fin_serie = series.get("end_at", "Date de début inconnue")[0:10]
            heure_fin_serie = series.get("end_at", "Heure de début inconnue")[11:19]
            date_modif_serie = series.get("modified_at", "Date de modification inconnue")[0:10]
            heure_modif_serie = series.get("modified_at", "Heure de modification inconnue")[11:19]     
            
            # Adversaires
            adversaires = match.get("opponents") or []
            if isinstance(adversaires, dict):
                adversaires = [adversaires]
            opponents_metadata = []
            
            if not adversaires:
                opponents_metadata = "Pas d'informations sur les concurrents"
            else:
                for adversaire in adversaires:
                    if not isinstance(adversaire,dict):
                        continue
                    opponent = adversaire.get("opponent")
                    
                    id_opponent = opponent.get("id","Id inconnu")
                    nom_opponent = opponent.get("name", "Nom incconu")
                    localisation_opponent = opponent.get("location","Localisation inconnue")
                    acronym_opponent = opponent.get("acronym","Acronyme inconnu")
                    date_modif_opponent = opponent.get("modified_at", "Date de modification inconnue")[0:10]
                    heure_modif_opponent = opponent.get("modified_at", "Heure de modification inconnue")[11:19]     
                    
                    opponents_metadata.append({
                        "ID": id_opponent,
                        "NOM": nom_opponent,
                        "LOCALISATION": localisation_opponent,
                        "ACRONYME": acronym_opponent,
                        "DATE DE LA DERNIERE MODIFICATION": date_modif_opponent,
                        "HEURE DE LA DERNIERE MODIFICATION": heure_modif_opponent,
                    })
            
            
            # Résultat      
            resultats = match.get("results") or []
            if isinstance(resultats, dict):
                resultats = [resultats]
            resultats_metadata = []
            
            if not resultats:
                resultats_metadata = "Pas de resultats disponibles"
            else:
                for resultat in resultats:
                    if not isinstance(adversaire,dict):
                        continue  
                    
                    score_result = resultat.get("score","Score inconnu")     
                    id_equipe = resultat.get("team_id","Id de l'equipe inconnu")     
                    
                    resultats_metadata.append({
                        "SCORE": score_result,
                        "ID EQUIPE": id_equipe
                    })
            
            # Création du dossier de la league
            dossier_league = os.path.join(DOSSIER_PRINCIPAL, f"{moment}", f"{jeu}", f"{nom}")
            os.makedirs(dossier_league, exist_ok=True)
            
            # Chemin complet du fichier JSON pour la league
            chemin_fichier_json = os.path.join(dossier_league, f"{id}.json")
            
            
            # Metadonnées et informations de la league
            metadata= {
                "DONNEES GENERALES DU MATCH": {
                    "ID": id,
                    "NOM": nom,
                    "JEU VIDEO": jeu,
                    "VERSION ACTUELLE DU JEU": version,
                    "STATUT": statut,
                    "NOMBRE DE PARTIE": nb_games,
                    "DATE DE DEBUT": date_debut,
                    "HEURE DE DEBUT": heure_debut,
                    "DATE DE FIN": date_fin,
                    "HEURE DE FIN": heure_fin,
                    "DATE DE MODIFICATION": date_modif_serie,
                    "HEURE DE MODIFICATION": heure_modif_serie,
                    "STATS DETAILLEES": stats_detail,
                    "LIVE": {
                        "SUPPORT": support,
                        "OUVERTURE": ouverture,
                    },
                    "AVANTAGE DURANT LA PARTIE": avantage_partie
                },
                
                "PARTIES": parties,
                
                "ADVERSAIRES": opponents_metadata,
                
                "RESULTATS": resultats_metadata,
                
               "TOURNOI": {
                    "ID": id_tournoi,
                    "NOM": nom_tournoi,
                    "TYPE": type_tournoi,
                    "PAYS": pays_tournoi,
                    "REGION": region_tournoi,
                    "TIER": tier_tournoi,
                    "CASH PRIZE": cash_prize_tournoi,
                    "VAINQUEUR": winner_tournoi,
                    "DATE DE DEBUT": date_debut_tournoi,
                    "HEURE DE DEBUT": heure_debut_tournoi,
                    "DATE DE FIN": date_fin_tournoi,
                    "HEURE DE FIN": heure_fin_tournoi,
                    "DATE DE MODIFICATION": date_modif_tournoi,
                    "HEURE DE MODIFICATION": heure_modif_tournoi,
                    "STATS DETAILLEES": stat_detail_tournoi,
                    "LIVE SUPPORT": live_supported_tournoi
                },
               
               "LIGUE": {
                    "ID": id_ligue,
                    "NOM": nom_ligue,
                    "DATE DE MODIFICATION": date_modif_ligue,
                    "HEURE DE MODIFICATION": heure_modif_ligue
                },         
                      
                "SERIE": {
                    "ID": id_serie,
                    "NOM": nom_serie,
                    "ANNEE": annee_serie,
                    "VAINQUEUR": winner_serie,
                    "DATE DE DEBUT": date_debut_serie,
                    "HEURE DE DEBUT": heure_debut_serie,
                    "DATE DE FIN": date_fin_serie,
                    "HEURE DE FIN": heure_fin_serie,
                    "DATE DE MODIFICATION": date_modif_serie,
                    "HEURE DE MODIFICATION": heure_modif_serie
                }
            }
            
            # Sauvegarde des données dans un fichier JSON
            with open(chemin_fichier_json, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, ensure_ascii=False, indent=4)
            print(f" Fichier cree '{nom}' sauvegardees dans '{chemin_fichier_json}'")
        
        except Exception as e:
            print(f" Erreur lors du traitement de la league '{nom}': {e}")