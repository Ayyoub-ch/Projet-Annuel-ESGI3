# Streamlit App

import streamlit as st
import requests
import json
import pandas as pd
import json
import datetime
import numpy as np

# ========================================
# Configuration
# ========================================
BASE_URL = "https://api-esport-sportsphere.onrender.com"

API_ESPORT = f"{BASE_URL}"

# ========================================
# VERIFICATION DE LA CONNECTION À L'API E-SPORT
# ========================================
def check_api_connection(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Vérifie si la requête a réussi (code 200)
        return True, response.json()  # Retourne True et les données JSON
    except requests.exceptions.RequestException as e:
        return False, str(e)  # Retourne False et le message d'erreur

# ========================================
# APPEL DE L'API E-SPORT
# ========================================
def fetch_data(endpoint, params=None):
    url = f"{BASE_URL}{endpoint}"
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 404:
            return None  # On renvoie gentiment None, sans rien afficher à l'écran
        
        response.raise_for_status()  # Vérifie si la requête a réussi (code 200)
        return response.json()  # Retourne les données JSON
    
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de l'appel à l'API : {e}")
        return None
    
# ========================================
# NETTOYE LES DONNÉES POUR LES COLONNES "EQUIPES", "MEMBRES DE L'EQUIPE" ET "MATCHES"
# ========================================
def extract_name(val):
  # 1. Si la cellule est un dictionnaire (ex: {'ID': 12617, 'NOM': '1.0mb', ...})
  if isinstance(val, dict):
    return val.get("NOM", str(val))

  # 2. Si la cellule est une liste de dictionnaires
  elif isinstance(val, list):
    names = [
        item.get("NOM", str(item)) if isinstance(item, dict) else str(item)
        for item in val
    ]
    return ", ".join(names)

  # 3. Si c'est du texte simple (ex: "Pas d'informations sur l'équipe") ou vide/NaN
  return str(val)




# ========================================
# VARIABLES POUR API E-SPORT
# ========================================

ESPORT_TYPES = ["Choisir une catégorie", "Ligues", "Series", "Tournois","Matchs" ]
moments_esport_classic = ["Choisir un moment", "Maintenant", "Par Période", "Par Date"]
moments_esport_match = ["Choisir un moment", "Maintenant", "Par Période", "Par Date", "Par Temps", "Annulé"]
jeux = ["Choisir un jeu", "Call of Duty", "Counter Strike", "Dota 2", "King of Glory", "League of Legends", 
        "Mobile Legends : Bang Bang", "Overwatch", "Rainbow 6 Siege", "Starcraft 2", "Valorant"]
times = ["Passé", "En cours", "A venir"]

st.title("SportSphere")

# ========================================
# Sidebar - Navigation
# ========================================

st.sidebar.title("Navigation")

# Vérification de la connexion de l'API
is_connected_esport, api_response_esport = check_api_connection(BASE_URL)

if is_connected_esport:
    st.sidebar.success("API E-Sport Connectée")
else:
    st.sidebar.error("API E-Sport Non disponible")
    
st.sidebar.markdown("---")

router_choice = st.sidebar.radio(
    "Choisir un service :",
    ["Accueil", "E-Sport"]
)

# On nettoie les données si on change de page
# clear_data_on_page_change(router_choice)


# ========================================
# Pages
# ========================================

if router_choice =="Accueil":
    st.header("Bienvenue sur l'interface SportSphere pour les données E-Sports")
    
    st.markdown("""
    Cette interface permet d'intéragir avec les APIs Open Data pour récupérer des données en lien
    avec le Sport. Cette version de l'interface se concentrera sur l'E-Sport
    
    ### Services disponibles
    
    | Service | Description |
    | ------- | ----------- |
    | **E-Sport** | Récupère les données de l'E-Sport |
    
    ### Statut des APIs 
    """)
    
    if is_connected_esport:
        st.success("L'API E-Sports est en ligne et opérationnelle.")
        st.json(api_response_esport)
    else:
        st.error("L'API E-Sports n'est pas accessible. Vérifiez qu'elle est bien lancée sur " + API_ESPORT)

elif router_choice == "E-Sport":
    
    category = st.selectbox("Catégorie :", ESPORT_TYPES)
    
    # =============
    # Ligues
    # =============
    if category == "Ligues" :
        st.header("Ligues")
        st.markdown("Récupère les données des ligues E-Sport. ")
        
        cat = "league"
        
        # Variables par défaut
        endpoint = None
        params = None
        filename = None
        
        moments = st.selectbox("Moment :", moments_esport_classic)
        
        if moments == "Maintenant":
            
            videogame = st.selectbox("Jeu Vidéo :", jeux)
            
            if videogame == "Call of Duty":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint)
                                                
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else:
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les ligues de Call of Duty pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                            }
                        )
                        st.write("Données récupérées pour Counter Strike avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

            
            elif videogame == "Counter Strike":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint)
                                                                    
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else:
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les ligues de Counter Strike pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                            "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                            "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                            "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                            "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                            "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                            "SERIE.ID": "ID Série",
                            "SERIE.NOM": "Nom de la Série",
                            "SERIE.ANNEE": "Année de la Série",
                            "SERIE.SAISON": "Saison de la Série",
                            "SERIE.DATE DE DEBUT": "Date de début",
                            "SERIE.HEURE DE DEBUT": "Heure de début",
                            "SERIE.DATE DE FIN": "Date de fin",
                            "SERIE.HEURE DE FIN": "Heure de fin"
                            }
                        )
                        st.write("Données récupérées pour Counter Strike avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                

            elif videogame == "Dota 2":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint)
                    
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else:
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les ligues de Dota 2 pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write("Données récupérées pour Dota 2 avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")


            elif videogame == "King of Glory":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint)
                                        
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les ligues de King of Glory pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write("Données récupérées pour King of Glory avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")


            elif videogame == "League of Legends":
                videogame = "LoL"
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint)
                                        
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les ligues de League of Legends pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write("Données récupérées pour League of Legends avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

            
            elif videogame == "Mobile Legends : Bang Bang":
                videogame = "Mobile Legends Bang Bang"
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else:
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les ligues de Mobile Legends : Bang Bang pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write("Données récupérées pour Mobile Legends : Bang Bang avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

            elif videogame == "Overwatch":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données"):
                    
                    api_response = fetch_data(endpoint)
                    
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else :
                    
                        df = pd.json_normalize(fetch_data(endpoint))
                        
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les ligues d'Overwatch pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write("Données récupérées pour Mobile Legends : Bang Bang avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")    
                    
                    
            elif videogame == "Rainbow 6 Siege":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données"):
                    
                    api_response = fetch_data(endpoint)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les ligues de Rainbow 6 Siege pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write("Données récupérées pour Rainbow 6 Siege avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

            
            elif videogame == "Starcraft 2":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                    api_response = fetch_data(endpoint)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                    
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les ligues Starcraft 2 pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write("Données récupérées pour Starcraft 2 avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                
            elif videogame == "Valorant":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                    api_response = fetch_data(endpoint)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue en cours trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour pour les ligues de {videogame} pour le moment.")
                            st.stop()
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write("Données récupérées pour Valorant avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")


        
        if moments == "Par Période":
            
            videogame = st.selectbox("Jeu Vidéo :", jeux)
            
            if videogame == "Call of Duty":
                date1 = st.date_input("Date de début :", value=datetime.date.today())
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue existante trouvée pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")


            elif videogame == "Counter Strike":
                date1 = st.date_input("Date de début :", value=datetime.date.today())
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                    api_response = fetch_data(endpoint,params)
                                                                                
                    if api_response is None:
                        st.warning(f"Aucune ligue trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
            elif videogame == "Dota 2":
                date1 = st.date_input("Date de début :", value=datetime.date.today())
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue trouvée pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
                
            elif videogame == "King of Glory":
                date1 = st.date_input("Date de début :", value=datetime.date.today())
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données"):
                    
                    api_response = fetch_data(endpoint,params)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
            elif videogame == "League of Legends":
                videogame = "LoL"
                date1 = st.date_input("Date de début :", value=datetime.date.today())
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
            elif videogame == "Mobile Legends : Bang Bang":
                videogame = "Mobile Legends Bang Bang"
                date1 = st.date_input("Date de début :", value=datetime.date.today())
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données"):
                    
                    api_response = fetch_data(endpoint,params)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
            elif videogame == "Overwatch":
                date1 = st.date_input("Date de début :", value=datetime.date.today())
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                    
                    if api_response is None:
                        st.warning(f"Aucune ligue trouvée pour {videogame}.")
                        st.stop()
                    else :
                    
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(api_response)
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(api_response)
                    if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
                
            elif videogame == "Rainbow 6 Siege":
                date1 = st.date_input("Date de début :", value=datetime.date(2026, 1, 1))
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue trouvée pour {videogame}.")
                        st.stop()
                    else:
                    
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
            elif videogame == "Starcraft 2":
                date1 = st.date_input("Date de début :", value=datetime.date(2026, 1, 1))
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données"):
                    
                    api_response = fetch_data(endpoint,params)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue trouvée pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
                
            elif videogame == "Valorant":
                date1 = st.date_input("Date de début :", value=datetime.date(2026, 1, 1))
                date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                params = {
                    "date1": date1,
                    "date2": date2
                }
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                                            
                    if api_response is None:
                        st.warning(f"Aucune ligue trouvée pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")


        if moments == "Par Date":
            
            videogame = st.selectbox("Jeu Vidéo :", jeux)
            
            if videogame == "Call of Duty":
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                                                                
                    if api_response is None:
                        st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                        st.stop()
                    else:
                    
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
            elif videogame == "Counter Strike":
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    
                    api_response = fetch_data(endpoint,params)
                                                                                
                    if api_response is None:
                        st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                        
            elif videogame == "Dota 2":
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                                                                
                    if api_response is None:
                        st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                        st.stop()
                    else:
                        
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
            elif videogame == "King of Glory":
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                                                                
                    if api_response is None:
                        st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                        st.stop()
                    else:
                        
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
            elif videogame == "League of Legends":
                videogame = "LoL"
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                    
                    if api_response is None:
                        st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour League of Legends pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                            }
                        )
                        st.write(f"Données récupérées pour League of Legends avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
            elif videogame == "Mobile Legends : Bang Bang":
                videogame = "Mobile Legends Bang Bang"
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    
                    api_response = fetch_data(endpoint,params)
                                        
                    if api_response is None:
                        st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour Mobile Legends : Bang Bang pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour Mobile Legends : Bang Bang avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
            
            
            elif videogame == "Overwatch":
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    
                    api_response = fetch_data(endpoint,params)
                    
                    
                    if api_response is None:
                        st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                        st.stop()
                    else :
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(api_response)
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
            
            elif videogame == "Rainbow 6 Siege":
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                        
                    if api_response is None:
                        st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
            elif videogame == "Starcraft 2":
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                        
                    if api_response is None:
                        st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
            elif videogame == "Valorant":
                date1 = st.date_input("Date :", value=datetime.date.today())
                params = {
                    "date1": date1
                }
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                if st.button("Récupérer les données"):
                    api_response = fetch_data(endpoint,params)
                                                            
                    if api_response is None:
                        st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                        st.stop()
                    else:
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                            
                        df = df.rename(
                            columns = {
                                "DONNEES GENERALES DE LA LIGUE.ID": "ID Ligue",
                                "DONNEES GENERALES DE LA LIGUE.NOM": "Nom de la Ligue",
                                "DONNEES GENERALES DE LA LIGUE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA LIGUE.VERSION ACTUELLE DU JEU": "Version Actuelle",
                                "DONNEES GENERALES DE LA LIGUE.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                "DONNEES GENERALES DE LA LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                
                                "SERIE.ID": "ID Série",
                                "SERIE.NOM": "Nom de la Série",
                                "SERIE.ANNEE": "Année de la Série",
                                "SERIE.SAISON": "Saison de la Série",
                                "SERIE.DATE DE DEBUT": "Date de début",
                                "SERIE.HEURE DE DEBUT": "Heure de début",
                                "SERIE.DATE DE FIN": "Date de fin",
                                "SERIE.HEURE DE FIN": "Heure de fin"
                                                    }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
                
    if category == "Series" :
            st.header("Séries")
            st.markdown("Récupère les données des séries E-Sport. ")
            
            cat = "serie"
            
            # Variables par défaut
            endpoint = None
            params = None
            filename = None
            
            moments = st.selectbox("Moment :", moments_esport_classic)
            
            if moments == "Maintenant":
                
                videogame = st.selectbox("Jeu Vidéo :", jeux)
                
                if videogame == "Call of Duty":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint)
                                                                
                        if api_response is None:
                            st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                            st.stop()
                        else:
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            # On vérifie si le DataFrame est vide avant de continuer
                            if df.empty:
                                st.warning("Aucune donnée disponible pour Call of Duty à ce moment.")
                                st.stop()
                                
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                                columns = {
                                    "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                    "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                    "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                    "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                                
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification de la Ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification de la Ligue",
                                    
                                    
                                }
                            )
                            st.write("Données récupérées pour Call of Duty avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
                elif videogame == "Counter Strike":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint)
                                                                                        
                        if api_response is None:
                            st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                            st.stop()
                        else:
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if df.empty:
                                st.warning("Aucune donnée disponible pour Counter Strike à ce moment.")
                                st.stop()
                                
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                                columns = {
                                    "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                    "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                    "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                    "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                                
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                    
                                    
                                }
                            )
                            
                            st.write("Données récupérées pour Counter Strike avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                            
                elif videogame == "Dota 2":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint)
                                                                                                                
                        if api_response is None:
                            st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                            st.stop()
                        else:
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if df.empty:
                                st.warning("Aucune donnée disponible pour Dota 2 à ce moment.")
                                st.stop()
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                                columns = {
                                    "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                    "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                    "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                    "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                                
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                    
                                    
                                }
                            )
                            
                            st.write("Données récupérées pour Dota 2 avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
                elif videogame == "King of Glory":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint)
                                                                                                                
                        if api_response is None:
                            st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                            st.stop()
                        else:
                            df = pd.json_normalize(fetch_data(endpoint))
                            if df.empty:
                                st.warning("Aucune donnée disponible pour King of Glory à ce moment.")
                                st.stop()
                                
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                                columns = {
                                    "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                    "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                    "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                    "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                                
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                    
                                    
                                }
                            )
                            st.write("Données récupérées pour King of Glory avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                
                elif videogame == "League of Legends":
                    videogame = "LoL"
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint)
                                                                                                                
                        if api_response is None:
                            st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                            st.stop()
                        else:
                            df = pd.json_normalize(fetch_data(endpoint))
                            if df.empty:
                                st.warning("Aucune donnée disponible pour League of Legends à ce moment.")
                                st.stop()
                                
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                                columns = {
                                    "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                    "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                    "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                    "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                                
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                    
                                }
                            )
                            st.write("Données récupérées pour League of Legends avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                
                elif videogame == "Mobile Legends : Bang Bang":
                    videogame = "Mobile Legends Bang Bang"
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint)
                                                                                                                
                        if api_response is None:
                            st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                            st.stop()
                        else:
                            df = pd.json_normalize(fetch_data(endpoint))
                            if df.empty:
                                st.warning("Aucune donnée disponible pour Mobile Legends : Bang Bang à ce moment.")
                                st.stop()
                                
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])    
                            
                            df_tn = df_tn.rename(
                            columns = {
                                "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                            
                                "LIGUE.ID": "ID Ligue",
                                "LIGUE.NOM": "Nom de la Ligue",
                                "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                
                            }
                        )
                            st.write("Données récupérées pour Mobile Legends : Bang Bang avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
                elif videogame == "Overwatch":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        
                        api_response = fetch_data(endpoint)
                                                    
                        if api_response is None:
                            st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                            st.stop()
                        else :
                        
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if df.empty:
                                st.warning("Aucune donnée disponible pour Dota 2 à ce moment.")
                                st.stop()
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                                columns = {
                                    "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                    "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                    "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                    "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                                
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                    
                                    
                                }
                            )
                            st.write("Données récupérées pour Rainbow 6 Siege avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
                
                
                
                
                elif videogame == "Rainbow 6 Siege":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint)
                                                                                                                
                        if api_response is None:
                            st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                            st.stop()
                        else:
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if df.empty:
                                st.warning("Aucune donnée disponible pour Dota 2 à ce moment.")
                                st.stop()
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                                columns = {
                                    "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                    "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                    "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                    "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                                
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                    
                                    
                                }
                            )
                            st.write("Données récupérées pour Rainbow 6 Siege avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                
                elif videogame == "Starcraft 2":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint)
                                                                                                                
                        if api_response is None:
                            st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                            st.stop()
                        else:
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if df.empty:
                                st.warning("Aucune donnée disponible pour Dota 2 à ce moment.")
                                st.stop()
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df = df.rename(
                                columns = {
                                    "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                    "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                    "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                    "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                                
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                    
                                }
                            )
                            st.write("Données récupérées pour Starcraft 2 avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                                                    
                                                    
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
                elif videogame == "Valorant":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint)
                                                                                                                
                        if api_response is None:
                            st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                            st.stop()
                        else:
                        
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if df.empty:
                                st.warning("Aucune donnée disponible pour Dota 2 à ce moment.")
                                st.stop()
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                            
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                                                    
                            df_tn = df_tn.rename(
                                columns = {
                                    "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                    "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                    "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                    "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                    "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                                
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                    
                                    
                                }
                            )
                            
                            st.write("Données récupérées pour Dota 2 avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
            if moments == "Par Période":
                
                videogame = st.selectbox("Jeu Vidéo :", jeux)
            
                if videogame == "Call of Duty":
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                        
                elif videogame == "Counter Strike":
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                            
                elif videogame == "Dota 2":
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
                    
                elif videogame == "King of Glory":
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint,params)
                                                                            
                        if api_response is None:
                            st.warning(f"Aucune série trouvée pour {videogame}.")
                            st.stop()
                        else:
                        
                            date1_str = date1.strftime("%Y-%m-%d")
                            date2_str = date2.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}&date2={date2_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                st.stop()
                            
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                                                    
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                            columns = {
                                "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                            
                                "LIGUE.ID": "ID Ligue",
                                "LIGUE.NOM": "Nom de la Ligue",
                                "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                
                                
                                }
                            )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint, params=params))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                
                elif videogame == "League of Legends":
                    videogame = "LoL"
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                
                elif videogame == "Mobile Legends : Bang Bang":
                    videogame = "Mobile Legends Bang Bang"
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                elif videogame == "Overwatch":
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données"):
                        api_response = fetch_data(endpoint,params)
                                                    
                        if api_response is None:
                            st.warning(f"Aucune série trouvée pour {videogame}.")
                            st.stop()
                        else:
                            date1_str = date1.strftime("%Y-%m-%d")
                            date2_str = date2.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}&date2={date2_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                st.stop()
                            
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                                                    
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                            columns = {
                                "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                            
                                "LIGUE.ID": "ID Ligue",
                                "LIGUE.NOM": "Nom de la Ligue",
                                "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                
                                
                                }
                            )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint, params=params))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                        
                                        
                                        
                                            
                elif videogame == "Rainbow 6 Siege":
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                
                elif videogame == "Starcraft 2":
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                    
                elif videogame == "Valorant":
                    date1 = st.date_input("Date de début :", value=datetime.date.today())
                    date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                    params = {
                        "date1": date1,
                        "date2": date2
                    }
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        date2_str = date2.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}&date2={date2_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                      
    
            if moments == "Par Date":
                            
                videogame = st.selectbox("Jeu Vidéo :", jeux)
            
                if videogame == "Call of Duty":
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                        
                        
                        
                elif videogame == "Counter Strike":
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                            
                elif videogame == "Dota 2":
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
                elif videogame == "King of Glory":
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
                elif videogame == "League of Legends":
                    videogame = "LoL"
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour League of Legends pour cette date.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour League of Legends avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
                elif videogame == "Mobile Legends : Bang Bang":
                    videogame = "Mobile Legends Bang Bang"
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour Mobile Legends : Bang Bang pour cette date.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour Mobile Legends : Bang Bang avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
                
                elif videogame == "Overwatch":
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données"):
                        
                        api_response = fetch_data(endpoint,params)
                        
                        if api_response is None:
                            st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                            st.stop()
                        else :
                            date1_str = date1.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}"
                            df = pd.json_normalize(api_response)
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                st.stop()
                            
                            # Suppression de la colonne Tournois pour l'affichage
                            df_tn = df.drop(columns=["TOURNOIS"])
                                                    
                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                            tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                            
                            df_tn = df_tn.rename(
                            columns = {
                                "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                                "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                                "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                                "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                                "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                                "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                                "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                                "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                                "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                            
                                "LIGUE.ID": "ID Ligue",
                                "LIGUE.NOM": "Nom de la Ligue",
                                "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                                "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                                
                                
                                }
                            )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_tn)
                            st.write("Données des tournois :")
                            st.dataframe(tournois_details)
                            
                            st.write("Données brutes :")
                            st.json(api_response)
                        if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
                
                elif videogame == "Rainbow 6 Siege":
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                
                elif videogame == "Starcraft 2":
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
                elif videogame == "Valorant":
                    date1 = st.date_input("Date :", value=datetime.date.today())
                    params = {
                        "date1": date1
                    }
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                        date1_str = date1.strftime("%Y-%m-%d")
                        params = f"date1={date1_str}"
                        df = pd.json_normalize(fetch_data(endpoint, params=params))
                        
                        if df.empty:
                            st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                            st.stop()
                        
                        # Suppression de la colonne Tournois pour l'affichage
                        df_tn = df.drop(columns=["TOURNOIS"])
                                                
                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                        df_exploded = df.explode("TOURNOIS").reset_index(drop=True)
                        tournois_details = pd.json_normalize(df_exploded["TOURNOIS"])
                        
                        df_tn = df_tn.rename(
                        columns = {
                            "DONNEES GENERALES DE LA SERIE.ID": "ID Série",
                            "DONNEES GENERALES DE LA SERIE.NOM": "Nom de la Série",
                            "DONNEES GENERALES DE LA SERIE.JEU VIDEO": "Jeu Vidéo",
                            "DONNEES GENERALES DE LA SERIE.ANNEE": "Année de la Série",
                            "DONNEES GENERALES DE LA SERIE.SAISON": "Saison de la Série",
                            "DONNEES GENERALES DE LA SERIE.DATE DE DEBUT": "Date de début",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE DEBUT": "Heure de début",
                            "DONNEES GENERALES DE LA SERIE.DATE DE FIN": "Date de fin",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE FIN": "Heure de fin",
                            "DONNEES GENERALES DE LA SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de la dernière modification",
                            "DONNEES GENERALES DE LA SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de la dernière modification",
                        
                            "LIGUE.ID": "ID Ligue",
                            "LIGUE.NOM": "Nom de la Ligue",
                            "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date dernière modification Ligue",
                            "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure dernière modification Ligue",
                            
                            
                            }
                        )
                        st.write(f"Données récupérées pour {videogame} avec succès !")
                        st.dataframe(df_tn)
                        st.write("Données des tournois :")
                        st.dataframe(tournois_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint, params=params))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint, params=params), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")   
                    
                    
    if category == "Tournois" :
                st.header("Tournois")
                st.markdown("Récupère les données des tournois E-Sport. ")
                
                cat = "tournament"
                
                # Variables par défaut
                endpoint = None
                params = None
                filename = None
                
                moments = st.selectbox("Moment :", moments_esport_classic)
                
                if moments == "Maintenant":
                    
                    videogame = st.selectbox("Jeu Vidéo :", jeux)
                    
                    if videogame == "Call of Duty":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                            df = pd.json_normalize(fetch_data(endpoint))
                            if df.empty:
                                st.warning("Aucune donnée disponible pour le moment.")
                                st.stop()
                            else:
                                
                                cols_to_drop = [c for c in ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"] if c in df.columns]
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            
                            if "EQUIPES" in df.columns:
                                equipes_val = df["EQUIPES"].iloc[0]
                                if not isinstance(equipes_val, str):
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    equipes_details = pd.json_normalize(df_e["EQUIPES"])
                                    st.write("Données des équipes :")
                                    st.dataframe(equipes_details)
                                    
                            if "MEMBRES DE L'EQUIPE" in df.columns:
                                membres_val = df["MEMBRES DE L'EQUIPE"].iloc[0]
                                if not isinstance(membres_val, str):
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    membres_equipes_details = pd.json_normalize(df_m["MEMBRES DE L'EQUIPE"], record_path=["JOUEURS"])
                                    st.write("Données des membres des équipes :")
                                    st.dataframe(membres_equipes_details)
                                    
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                            
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
                    elif videogame == "Counter Strike":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if df.empty:
                                st.warning("Aucune donnée disponible pour le moment.")
                                st.stop()
                            else:
                                
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # Si ce sont des dicts, on normalise. Sinon, on transforme en DataFrame simple.
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                 
                                equipes_details = pd.json_normalize(df_e["EQUIPES"])
                                
                                equipes_details = pd.json_normalize(df_e["EQUIPES"])    
                                    
                                    
                                if df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict)).any():
                                   membres_equipes_details = pd.json_normalize(df_m["MEMBRES DE L'EQUIPE"], record_path=["JOUEURS"], errors='ignore')
                                else:
                                    membres_equipes_details = pd.DataFrame(df_m["MEMBRES DE L'EQUIPE"])     
                                    
                                    
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write("Données récupérées pour Counter Strike avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)

                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                            
                    elif videogame == "Dota 2":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if df.empty:
                                st.warning("Aucune donnée disponible pour le moment.")
                                st.stop()
                            else:
                                
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # transition
                                equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(equipes_propres)
                                membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                                                        
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                        
                    elif videogame == "King of Glory":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else :          
                            
                                df = pd.json_normalize(fetch_data(endpoint))
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(df_e["EQUIPES"])
                                    membres_equipes_details = pd.json_normalize(df_m["MEMBRES DE L'EQUIPE"],record_path=["JOUEURS"])
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des matchs :")
                                st.dataframe(matchs_details)
                                st.write("Données des équipes :")
                                st.dataframe(equipes_details)
                                st.write("Données des membres des équipes :")
                                st.dataframe(membres_equipes_details)
                                                            
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint))
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
                    
                    elif videogame == "League of Legends":
                        videogame = "LoL"
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint)
                            
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else :
                                                
                                df = pd.json_normalize(fetch_data(endpoint))
                                
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(df_e["EQUIPES"])
                                    membres_equipes_details = pd.json_normalize(df_m["MEMBRES DE L'EQUIPE"],record_path=["JOUEURS"])
                                
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )
                                st.write(f"Données récupérées pour League of Legends avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des matchs :")
                                st.dataframe(matchs_details)
                                st.write("Données des équipes :")
                                st.dataframe(equipes_details)
                                st.write("Données des membres des équipes :")
                                st.dataframe(membres_equipes_details)
                                                            
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint))
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
                        
                    elif videogame == "Mobile Legends : Bang Bang":
                        videogame = "Mobile Legends  Bang Bang"
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if df.empty:
                                st.warning("Aucune donnée disponible pour le moment.")
                                st.stop()
                            else:
                                
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(df_e["EQUIPES"])
                                membres_equipes_details = pd.json_normalize(df_m["MEMBRES DE L'EQUIPE"],record_path=["JOUEURS"])
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour Mobile Legends : Bang Bang avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                                                        
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                    
                    elif videogame == "Overwatch":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if df.empty:
                                st.warning("Aucune donnée disponible pour le moment.")
                                st.stop()
                            else:
                                
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(df_e["EQUIPES"])
                                membres_equipes_details = pd.json_normalize(df_m["MEMBRES DE L'EQUIPE"],record_path=["JOUEURS"])
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                                                        
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
                    
                        
                    elif videogame == "Rainbow 6 Siege":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if df.empty:
                                st.warning("Aucune donnée disponible pour le moment.")
                                st.stop()
                            else:
                                
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(df_e["EQUIPES"])
                                membres_equipes_details = pd.json_normalize(df_m["MEMBRES DE L'EQUIPE"],record_path=["JOUEURS"])
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                                                        
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                    
                    elif videogame == "Starcraft 2":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint)
                            
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else:
                            
                                df = pd.json_normalize(api_response)
                                
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    cols_to_drop = [c for c in ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"] if c in df.columns]
                                    
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des matchs :")
                                st.dataframe(matchs_details)
                                if "EQUIPES" in df.columns:
                                    equipes_val = df["EQUIPES"].iloc[0]
                                    if not isinstance(equipes_val, str):
                                        df_e = df.explode("EQUIPES").reset_index(drop=True)
                                        equipes_details = pd.json_normalize(df_e["EQUIPES"])
                                        st.write("Données des équipes :")
                                        st.dataframe(equipes_details)

                                if "MEMBRES DE L'EQUIPE" in df.columns:
                                     membres_val = df["MEMBRES DE L'EQUIPE"].iloc[0]
                                     if not isinstance(membres_val, str):
                                        df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                        membres_equipes_details = pd.json_normalize(df_m["MEMBRES DE L'EQUIPE"], record_path=["JOUEURS"])
                                        st.write("Données des membres des équipes :")
                                        st.dataframe(membres_equipes_details)

                                st.write("Données brutes :")
                                st.json(api_response)
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
            
                        
                    elif videogame == "Valorant":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if df.empty:
                                st.warning("Aucune donnée disponible pour le moment.")
                                st.stop()
                            else:
                                
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(df_e["EQUIPES"])
                                membres_equipes_details = pd.json_normalize(df_m["MEMBRES DE L'EQUIPE"],record_path=["JOUEURS"])
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                                                        
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                if moments == "Par Période":
                    
                    videogame = st.selectbox("Jeu Vidéo :", jeux)
                    
                    if videogame == "Call of Duty":     
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            date2_str = date2.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}&date2={date2_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                st.stop()
                            else:
                                                            
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # transition
                                equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(equipes_propres)
                                membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint, params))
                            
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")


                    if videogame == "Counter Strike":     
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            date2_str = date2.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}&date2={date2_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                st.stop()
                            else:
                                                            
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # transition
                                equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(equipes_propres)
                                membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint, params))
                            
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                            
                    if videogame == "Dota 2":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            date2_str = date2.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}&date2={date2_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                st.stop()
                            else:
                                                            
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # transition
                                equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(equipes_propres)
                                membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint, params))
                            
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")     
                    
                    if videogame == "King of Glory":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                            
                            if api_response is None:
                                st.warning(f"Aucun tournoi trouvé pour {videogame}.")
                                st.stop()
                            else :                    
                                date1_str = date1.strftime("%Y-%m-%d")
                                date2_str = date2.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}&date2={date2_str}"
                                df = pd.json_normalize(fetch_data(endpoint, params=params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                    st.stop()
                                else:
                                                                
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des matchs :")
                                st.dataframe(matchs_details)
                                st.write("Données des équipes :")
                                st.dataframe(equipes_details)
                                st.write("Données des membres des équipes :")
                                st.dataframe(membres_equipes_details)
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")  
                            
                                   
                    if videogame == "League of Legends":
                        videogame = "Lol"
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun tournoi trouvé pour {videogame}.")
                                st.stop()
                            else :
                            
                                date1_str = date1.strftime("%Y-%m-%d")
                                date2_str = date2.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}&date2={date2_str}"
                                df = pd.json_normalize(fetch_data(endpoint, params=params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                    st.stop()
                                else:
                                                                
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )
                                st.write("Données récupérées pour League of Legends avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des matchs :")
                                st.dataframe(matchs_details)
                                st.write("Données des équipes :")
                                st.dataframe(equipes_details)
                                st.write("Données des membres des équipes :")
                                st.dataframe(membres_equipes_details)
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")  
                            
                    if videogame == "Mobile Legends : Bang Bang":
                        videogame = "Mobile Legends Bang Bang"
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                                                
                            if api_response is None:
                                st.warning(f"Aucune série trouvée pour {videogame}.")
                                st.stop()
                            else:
                                date1_str = date1.strftime("%Y-%m-%d")
                                date2_str = date2.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}&date2={date2_str}"
                                df = pd.json_normalize(fetch_data(endpoint, params=params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                    st.stop()
                                else:
                                                                
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )
                                st.write("Données récupérées pour Mobile Legends : Bang Bang avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des matchs :")
                                st.dataframe(matchs_details)
                                st.write("Données des équipes :")
                                st.dataframe(equipes_details)
                                st.write("Données des membres des équipes :")
                                st.dataframe(membres_equipes_details)
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")          
                                
                            
                    
                    if videogame == "Overwatch":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun tournoi trouvé pour {videogame}.")
                                st.stop()
                            else :
                            
                                date1_str = date1.strftime("%Y-%m-%d")
                                date2_str = date2.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}&date2={date2_str}"
                                df = pd.json_normalize(api_response)
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                    st.stop()
                                else:
                                                                
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des matchs :")
                                st.dataframe(matchs_details)
                                st.write("Données des équipes :")
                                st.dataframe(equipes_details)
                                st.write("Données des membres des équipes :")
                                st.dataframe(membres_equipes_details)
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")   
                    
                    
                           
                    if videogame == "Rainbow 6 Siege":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            date2_str = date2.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}&date2={date2_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                st.stop()
                            else:
                                                            
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # transition
                                equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(equipes_propres)
                                membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint, params))
                            
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")   
                            
                            
                    if videogame == "Starcraft 2":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            date2_str = date2.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}&date2={date2_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                st.stop()
                            else:
                                                            
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # transition
                                equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(equipes_propres)
                                membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint, params))
                            
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")  
                    
                    if videogame == "Valorant":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"tournois_{videogame}_period.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            date2_str = date2.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}&date2={date2_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2} pour {videogame}.")
                                st.stop()
                            else:
                                                            
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # transition
                                equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(equipes_propres)
                                membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des matchs :")
                            st.dataframe(matchs_details)
                            st.write("Données des équipes :")
                            st.dataframe(equipes_details)
                            st.write("Données des membres des équipes :")
                            st.dataframe(membres_equipes_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint, params))
                            
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")  
                            
                if moments == "Par Date":
                            
                    videogame = st.selectbox("Jeu Vidéo :", jeux)
                    
                    if videogame == "Call of Duty":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                st.stop()
                            else:
                                # Suppression de la colonne Tournois pour l'affichage
                                df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                
                                
                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                df_e = df.explode("EQUIPES").reset_index(drop=True)
                                df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                
                                # transition
                                equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                equipes_details = pd.json_normalize(equipes_propres)
                                membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )
                                # st.write(df.columns.tolist())

                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des matchs :")
                                st.dataframe(matchs_details)
                                st.write("Données des équipes :")
                                st.dataframe(equipes_details)
                                st.write("Données des membres des équipes :")
                                st.dataframe(membres_equipes_details)
                                
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                
                    elif videogame == "Counter Strike":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                st.stop()
                            else:
                                colonnes_supplementaires = ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"]
                                # On n'exécute le drop que si TOUTES les colonnes sont bien présentes
                                if all(col in df.columns for col in colonnes_supplementaires):
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )

                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                if "MATCHES" in df.columns:
                                    st.write("Données des matchs :")
                                    st.dataframe(matchs_details)
                                if "EQUIPES" in df.columns:
                                    st.write("Données des équipes :")
                                    st.dataframe(equipes_details)
                                if "MEMBRES DE L'EQUIPE" in df.columns:
                                    st.write("Données des membres des équipes :")
                                    st.dataframe(membres_equipes_details)
                                
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                
                    elif videogame == "Dota 2":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                st.stop()
                            else:
                                colonnes_supplementaires = ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"]
                                # On n'exécute le drop que si TOUTES les colonnes sont bien présentes
                                if all(col in df.columns for col in colonnes_supplementaires):
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )

                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                if "MATCHES" in df.columns:
                                    st.write("Données des matchs :")
                                    st.dataframe(matchs_details)
                                if "EQUIPES" in df.columns:
                                    st.write("Données des équipes :")
                                    st.dataframe(equipes_details)
                                if "MEMBRES DE L'EQUIPE" in df.columns:
                                    st.write("Données des membres des équipes :")
                                    st.dataframe(membres_equipes_details)
                                
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                        
                    elif videogame == "King of Glory":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            
                            api_response = fetch_data(endpoint, params=params)
                            
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else :
                            
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                df = pd.json_normalize(api_response)
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                    st.stop()
                                else:
                                    colonnes_supplementaires = ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"]
                                    # On n'exécute le drop que si TOUTES les colonnes sont bien présentes
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression de la colonne Tournois pour l'affichage
                                        df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                        
                                        
                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                        df_e = df.explode("EQUIPES").reset_index(drop=True)
                                        df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                        
                                        # transition
                                        equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                        membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                        
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                        equipes_details = pd.json_normalize(equipes_propres)
                                        membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                        
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )

                                    st.write(f"Données récupérées pour {videogame} avec succès !")
                                    st.dataframe(df_l)
                                    if "MATCHES" in df.columns:
                                        st.write("Données des matchs :")
                                        st.dataframe(matchs_details)
                                    if "EQUIPES" in df.columns:
                                        st.write("Données des équipes :")
                                        st.dataframe(equipes_details)
                                    if "MEMBRES DE L'EQUIPE" in df.columns:
                                        st.write("Données des membres des équipes :")
                                        st.dataframe(membres_equipes_details)
                                    
                                    
                                    st.write("Données brutes :")
                                    st.json(fetch_data(endpoint, params))
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")


                    elif videogame == "League of Legends":
                        videogame = "LoL"
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            
                            api_response = fetch_data(endpoint, params=params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun tournois trouvé pour {videogame}.")
                                st.stop()
                            else :
                            
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                df = pd.json_normalize(fetch_data(endpoint, params=params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                    st.stop()
                                else:
                                    colonnes_supplementaires = ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"]
                                    # On n'exécute le drop que si TOUTES les colonnes sont bien présentes
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression de la colonne Tournois pour l'affichage
                                        df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                        
                                        
                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                        df_e = df.explode("EQUIPES").reset_index(drop=True)
                                        df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                        
                                        # transition
                                        equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                        membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                        
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                        equipes_details = pd.json_normalize(equipes_propres)
                                        membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                        
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )

                                    st.write(f"Données récupérées pour {videogame} avec succès !")
                                    st.dataframe(df_l)
                                    if "MATCHES" in df.columns:
                                        st.write("Données des matchs :")
                                        st.dataframe(matchs_details)
                                    if "EQUIPES" in df.columns:
                                        st.write("Données des équipes :")
                                        st.dataframe(equipes_details)
                                    if "MEMBRES DE L'EQUIPE" in df.columns:
                                        st.write("Données des membres des équipes :")
                                        st.dataframe(membres_equipes_details)
                                    
                                    
                                    st.write("Données brutes :")
                                    st.json(fetch_data(endpoint, params))
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                        
                        
                    elif videogame == "Mobile Legends : Bang Bang":
                        videogame = "Mobile Legends  Bang Bang"
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                st.stop()
                            else:
                                colonnes_supplementaires = ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"]
                                # On n'exécute le drop que si TOUTES les colonnes sont bien présentes
                                if all(col in df.columns for col in colonnes_supplementaires):
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )

                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                if "MATCHES" in df.columns:
                                    st.write("Données des matchs :")
                                    st.dataframe(matchs_details)
                                if "EQUIPES" in df.columns:
                                    st.write("Données des équipes :")
                                    st.dataframe(equipes_details)
                                if "MEMBRES DE L'EQUIPE" in df.columns:
                                    st.write("Données des membres des équipes :")
                                    st.dataframe(membres_equipes_details)
                                
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                        
                    
                    
                    elif videogame == "Overwatch":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint,params)
                            
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                df = pd.json_normalize(fetch_data(endpoint, params=params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                    st.stop()
                                else:
                                    colonnes_supplementaires = ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"]
                                    # On n'exécute le drop que si TOUTES les colonnes sont bien présentes
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression de la colonne Tournois pour l'affichage
                                        df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                        
                                        
                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                        df_e = df.explode("EQUIPES").reset_index(drop=True)
                                        df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                        
                                        # transition
                                        equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                        membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                        
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                        equipes_details = pd.json_normalize(equipes_propres)
                                        membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                        
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                    columns={
                                        # Données générales du tournoi
                                        "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                        "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                        "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                        "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                        "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                        "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                        # Données de la ligue 
                                        "LIGUE.NOM": "Nom de la ligue",
                                        "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                        "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                        # Données de la série
                                        "SERIE.NOM": "Nom de la série",
                                        "SERIE.ANNEE": "Année de la série",
                                        "SERIE.SAISON": "Saison de la série",
                                        "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                        "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                        "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                    }
                            )

                                    st.write(f"Données récupérées pour {videogame} avec succès !")
                                    st.dataframe(df_l)
                                    if "MATCHES" in df.columns:
                                        st.write("Données des matchs :")
                                        st.dataframe(matchs_details)
                                    if "EQUIPES" in df.columns:
                                        st.write("Données des équipes :")
                                        st.dataframe(equipes_details)
                                    if "MEMBRES DE L'EQUIPE" in df.columns:
                                        st.write("Données des membres des équipes :")
                                        st.dataframe(membres_equipes_details)
                                    
                                    
                                    st.write("Données brutes :")
                                    st.json(fetch_data(endpoint, params))
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                        
                    
                    
                    
                    elif videogame == "Rainbow 6 Siege":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                st.stop()
                            else:
                                colonnes_supplementaires = ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"]
                                # On n'exécute le drop que si TOUTES les colonnes sont bien présentes
                                if all(col in df.columns for col in colonnes_supplementaires):
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )

                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                if "MATCHES" in df.columns:
                                    st.write("Données des matchs :")
                                    st.dataframe(matchs_details)
                                if "EQUIPES" in df.columns:
                                    st.write("Données des équipes :")
                                    st.dataframe(equipes_details)
                                if "MEMBRES DE L'EQUIPE" in df.columns:
                                    st.write("Données des membres des équipes :")
                                    st.dataframe(membres_equipes_details)
                                
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
                    
                    
                    
                    
                    elif videogame == "Starcraft 2":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                st.stop()
                            else:
                                colonnes_supplementaires = ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"]
                                # On n'exécute le drop que si TOUTES les colonnes sont bien présentes
                                if all(col in df.columns for col in colonnes_supplementaires):
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )

                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                if "MATCHES" in df.columns:
                                    st.write("Données des matchs :")
                                    st.dataframe(matchs_details)
                                if "EQUIPES" in df.columns:
                                    st.write("Données des équipes :")
                                    st.dataframe(equipes_details)
                                if "MEMBRES DE L'EQUIPE" in df.columns:
                                    st.write("Données des membres des équipes :")
                                    st.dataframe(membres_equipes_details)
                                
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                        
                    elif videogame == "Valorant":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"tournois_{videogame}_date.json"
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,params)):
                            date1_str = date1.strftime("%Y-%m-%d")
                            params = f"date1={date1_str}"
                            df = pd.json_normalize(fetch_data(endpoint, params=params))
                            
                            if df.empty:
                                st.warning(f"Aucune donnée disponible pour {videogame} pour cette date.")
                                st.stop()
                            else:
                                colonnes_supplementaires = ["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"]
                                # On n'exécute le drop que si TOUTES les colonnes sont bien présentes
                                if all(col in df.columns for col in colonnes_supplementaires):
                                    # Suppression de la colonne Tournois pour l'affichage
                                    df_l = df.drop(columns=["MATCHES", "EQUIPES", "MEMBRES DE L'EQUIPE"])
                                    
                                    
                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_mt_exploded = df.explode("MATCHES").reset_index(drop=True)
                                    df_e = df.explode("EQUIPES").reset_index(drop=True)
                                    df_m = df.explode("MEMBRES DE L'EQUIPE").reset_index(drop=True)
                                    
                                    # transition
                                    equipes_propres = df_e["EQUIPES"][df_e["EQUIPES"].apply(lambda x: isinstance(x, dict))]
                                    membres_propres = df_m["MEMBRES DE L'EQUIPE"][df_m["MEMBRES DE L'EQUIPE"].apply(lambda x: isinstance(x, dict))]
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    matchs_details = pd.json_normalize(df_mt_exploded["MATCHES"])
                                    equipes_details = pd.json_normalize(equipes_propres)
                                    membres_equipes_details = pd.json_normalize(membres_propres, record_path=["JOUEURS"])
                                    
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                columns={
                                    # Données générales du tournoi
                                    "DONNEES GENERALES DU TOURNOIS.ID": "ID Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.NOM": "Nom du Tournoi",
                                    "DONNEES GENERALES DU TOURNOIS.JEU VIDEO": "Jeu Vidéo",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE DEBUT": "Date de début",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE DEBUT": "Heure de début",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE FIN": "Date de fin",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE FIN": "Heure de fin",
                                    "DONNEES GENERALES DU TOURNOIS.DATE DE LA DERNIERE MODIFICATION": "Dernière modification",
                                    "DONNEES GENERALES DU TOURNOIS.HEURE DE LA DERNIERE MODIFICATION": "Heure modification",
                                    "DONNEES GENERALES DU TOURNOIS.ANNEE": "Année",
                                    "DONNEES GENERALES DU TOURNOIS.SAISON": "Saison",
                                    # Données de la ligue 
                                    "LIGUE.NOM": "Nom de la ligue",
                                    "LIGUE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la ligue",
                                    "LIGUE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la ligue",
                                    # Données de la série
                                    "SERIE.NOM": "Nom de la série",
                                    "SERIE.ANNEE": "Année de la série",
                                    "SERIE.SAISON": "Saison de la série",
                                    "SERIE.DATE DE LA DERNIERE MODIFICATION": "Date de modification de la série",
                                    "SERIE.HEURE DE LA DERNIERE MODIFICATION": "Heure de modification de la série",
                                    "SERIE.ID DU VAINQUEUR": "ID du vainqueur de la série",
                                }
                        )

                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                if "MATCHES" in df.columns:
                                    st.write("Données des matchs :")
                                    st.dataframe(matchs_details)
                                if "EQUIPES" in df.columns:
                                    st.write("Données des équipes :")
                                    st.dataframe(equipes_details)
                                if "MEMBRES DE L'EQUIPE" in df.columns:
                                    st.write("Données des membres des équipes :")
                                    st.dataframe(membres_equipes_details)
                                
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint, params))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")            
                                                   
    if category == "Matchs" :
                st.header("Matchs")
                st.markdown("Récupère les données des matchs E-Sport. ")
                
                cat = "match"
                
                # Variables par défaut
                endpoint = None
                params = None
                filename = None
                
                moments = st.selectbox("Moment :", moments_esport_match)
                
                if moments == "Maintenant":
                    
                    videogame = st.selectbox("Jeu Vidéo :", jeux)
                    
                    if videogame == "Call of Duty":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if df.empty:
                                st.warning("Aucune donnée disponible pour le moment.")
                                st.stop()
                            else:
                                # Suppression des autres parties pour un affiche plus aéré
                                df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                df_p = df.explode("PARTIES").reset_index(drop=True)
                                df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                df_r = df.explode("RESULTATS").reset_index(drop=True)
                                
                                # Applatissement des colonnes imbriquées pour l'affichage
                                parties_details = pd.json_normalize(df_p["PARTIES"])
                                adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                
                                # Renommage des colonnes pour une meilleure lisibilité
                                df_l = df_l.rename(
                                    columns={
                                        "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                        "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                        "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                        "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                        "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                        "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                        "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                        "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                        "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                        "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                        "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                        "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                        "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                        
                                        "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                        "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                        
                                        "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                        
                                        # Tournoi
                                        "TOURNOI.ID": "ID Tournoi",
                                        "TOURNOI.NOM": "Nom du Tournoi", 
                                        "TOURNOI.TYPE": "Type du Tournoi", 
                                        "TOURNOI.PAYS": "Pays du Tournoi", 
                                        "TOURNOI.REGION": "Région du Tournoi", 
                                        "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                        "TOURNOI.TIER": "Tier du Tournoi", 
                                        "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                        "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                        "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                        "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                        "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                        "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                        "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                        "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                        "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                        
                                        # Ligue
                                        "LIGUE.ID": "ID Ligue",
                                        "LIGUE.NOM": "Nom de la Ligue",
                                        "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                        "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                        
                                        # Série
                                        "SERIE.ID": "ID Série",
                                        "SERIE.NOM": "Nom de la Série",
                                        "SERIE.ANNEE": "Année de la Série",
                                        "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                        "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                        "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                        "SERIE.DATE DE FIN": "Date de fin de la Série",
                                        "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                        "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                        "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                    }
                                )
                            
                            
                            st.write(f"Données récupérées pour {videogame} avec succès !")
                            st.dataframe(df_l)
                            st.write("Données des parties :")
                            st.dataframe(parties_details)
                            st.write("Données des adversaires :")
                            st.dataframe(adversaires_details)
                            st.write("Données des résultats des matchs :")
                            st.dataframe(resultats_details)
                            
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                            
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                
                            
                            
                    if videogame == "Counter Strike":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(fetch_data(endpoint))
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                            
                            
                    if videogame == "Dota 2":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(fetch_data(endpoint))
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                            
                            
                    if videogame == "King of Glory":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint)
                            
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")        
                     
                     
                    if videogame == "League of Legends":
                        videogame = "LoL"
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(fetch_data(endpoint))
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.name": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.current": "Version Actuelle" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour League of Legends avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")       
                            

                    if videogame == "Mobile Legends : Bang Bang":
                        videogame = "Mobile Legends  Bang Bang"
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun ligue en cours trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(fetch_data(endpoint))
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour League of Legends avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(fetch_data(endpoint))
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")   
                            

                    
                    if videogame == "Overwatch":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint)
                            
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")   
                    
                    
                    
                    if videogame == "Rainbow 6 Siege":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint)
                            
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")        
                                
                                
                                
                    if videogame == "Starcraft 2":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint)
                            
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.") 
                                
                                
                    if videogame == "Valorant":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"matchs_{videogame}_now.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint)
                            
                            if api_response is None:
                                st.warning(f"Aucun match en cours trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.name": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.current": "Version Actuelle" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.") 
        
        
                
                if moments == "Par Période":
                    
                    videogame = st.selectbox("Jeu Vidéo :", jeux)
                                        
                    if videogame == "Call of Duty":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.TIER": "Tier du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                
                            
                            
                    if videogame == "Counter Strike":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                            
                            
                    if videogame == "Dota 2":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                            
                            
                    if videogame == "King of Glory":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint,params)
                            
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")        
                        
                        
                    if videogame == "League of Legends":
                        videogame = "LoL"
                        
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.name": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.current": "Version Actuelle" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour League of Legends avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")       
                            

                    if videogame == "Mobile Legends : Bang Bang":
                        videogame = "Mobile Legends Bang Bang"
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour League of Legends avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")   
                            

                    
                    if videogame == "Overwatch":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint,params)
                            
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")   
                    
                    
                    
                    if videogame == "Rainbow 6 Siege":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint,params)
                            
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")        
                                
                                
                                
                    if videogame == "Starcraft 2":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint,params)
                            
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.") 
                                
                                
                    if videogame == "Valorant":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        date2 = st.date_input("Date de fin :", value=datetime.date(2026, 12, 31))
                        params = {
                            "date1": date1,
                            "date2": date2
                        }
                        endpoint = f"/{cat}/{videogame}/period"
                        filename = f"matchs_{videogame}_period.json"
                        
                        if st.button("Récupérer les données"):
                            
                            api_response = fetch_data(endpoint,params)
                            
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour entre le {date1} et le {date2}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.name": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.current": "Version Actuelle" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour {videogame} avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.") 
                    
                    
                    
                    
                    
                if moments == "Par Date":
                    
                    videogame = st.selectbox("Jeu Vidéo :", jeux)
                    
                    if videogame == "Call of Duty":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                   
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                    
                                
                            
                    if videogame == "Counter Strike":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                            
                    if videogame == "Dota 2":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                            
                    if videogame == "King of Glory":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                        
                    if videogame == "League of Legends":
                        videogame = "LoL"
                        
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.name": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.current": "Version Actuelle" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour League of Legends avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")       
                            

                    if videogame == "Mobile Legends : Bang Bang":
                        videogame = "Mobile Legends Bang Bang"
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            

                    
                    if videogame == "Overwatch":
                        date1 = st.date_input("Date de début :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                    
                    
                    if videogame == "Rainbow 6 Siege":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                                
                                
                    if videogame == "Starcraft 2":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                                
                    if videogame == "Valorant":
                        date1 = st.date_input("Date :", value=datetime.date.today())
                        params = {
                            "date1": date1,
                        }
                        endpoint = f"/{cat}/{videogame}/date"
                        filename = f"matchs_{videogame}_date.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                date1_str = date1.strftime("%Y-%m-%d")
                                params = f"date1={date1_str}"
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le {date1}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                    
                    
                    
                if moments == "Par Temps":
                    videogame = st.selectbox("Jeu Vidéo :", jeux)
                                        
                    if videogame == "Call of Duty":
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                df = pd.json_normalize(api_response)
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le temps {time}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                    
                                
                            
                    if videogame == "Counter Strike":
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :

                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning(f"Aucune donnée disponible pour le temps {time}.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                            
                    if videogame == "Dota 2":
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                            
                    if videogame == "King of Glory":
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                               
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                        
                    if videogame == "League of Legends":
                        videogame = "LoL"
                        
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                                                                                    
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else:
                                df = pd.json_normalize(api_response)
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour le moment.")
                                    st.stop()
                                else:
                                    # Suppression des autres parties pour un affiche plus aéré
                                    df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                    # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                    df_p = df.explode("PARTIES").reset_index(drop=True)
                                    df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                    df_r = df.explode("RESULTATS").reset_index(drop=True)
                                    
                                    # Applatissement des colonnes imbriquées pour l'affichage
                                    parties_details = pd.json_normalize(df_p["PARTIES"])
                                    adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                                    resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                                    
                                    # Renommage des colonnes pour une meilleure lisibilité
                                    df_l = df_l.rename(
                                        columns={
                                            "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                            "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                            "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.name": "Version du Jeu" ,
                                            "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU.current": "Version Actuelle" ,
                                            "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                            "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                            "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                            "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                            "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                            
                                            "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                            "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                            
                                            "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                            
                                            # Tournoi
                                            "TOURNOI.ID": "ID Tournoi",
                                            "TOURNOI.NOM": "Nom du Tournoi", 
                                            "TOURNOI.TYPE": "Type du Tournoi", 
                                            "TOURNOI.PAYS": "Pays du Tournoi", 
                                            "TOURNOI.REGION": "Région du Tournoi", 
                                            "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                            "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                            "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                            "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                            "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                            "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                            "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                            "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                            "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                            "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                            
                                            # Ligue
                                            "LIGUE.ID": "ID Ligue",
                                            "LIGUE.NOM": "Nom de la Ligue",
                                            "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                            "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                            
                                            # Série
                                            "SERIE.ID": "ID Série",
                                            "SERIE.NOM": "Nom de la Série",
                                            "SERIE.ANNEE": "Année de la Série",
                                            "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                            "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                            "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                            "SERIE.DATE DE FIN": "Date de fin de la Série",
                                            "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                            "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                            "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                        }
                                    )
                                
                                
                                st.write(f"Données récupérées pour League of Legends avec succès !")
                                st.dataframe(df_l)
                                st.write("Données des parties :")
                                st.dataframe(parties_details)
                                st.write("Données des adversaires :")
                                st.dataframe(adversaires_details)
                                st.write("Données des résultats des matchs :")
                                st.dataframe(resultats_details)
                                
                                st.write("Données brutes :")
                                st.json(api_response)
                                
                            if st.download_button(label="Télécharger les données",data=json.dumps(api_response, indent=4),file_name=filename,mime="application/json"):
                                st.success(f"Les données ont été téléchargées sous le nom {filename}.")       
                            

                    if videogame == "Mobile Legends : Bang Bang":
                        videogame = "Mobile Legends Bang Bang"
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour ce moment.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            

                    
                    if videogame == "Overwatch":
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour ce moment.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                    
                    
                    if videogame == "Rainbow 6 Siege":
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                               
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour ce moment.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                                
                                
                    if videogame == "Starcraft 2":
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                               
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour ce moment.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                                            
                                
                    if videogame == "Valorant":
                        selected_time = st.selectbox("Temps :", times)
                        time_by_label = {
                            "Passé": "past",
                            "En cours": "running",
                            "A venir": "upcoming",
                        }
                        time = time_by_label[selected_time]
                        params = {
                            "time": time,
                        }
                        endpoint = f"/{cat}/{videogame}/time"
                        filename = f"matchs_{videogame}_time.json"
                        
                        if st.button("Récupérer les données"):
                            api_response = fetch_data(endpoint,params)
                                                        
                            if api_response is None:
                                st.warning(f"Aucun match trouvé pour {videogame}.")
                                st.stop()
                            else :
                                
                                df = pd.json_normalize(fetch_data(endpoint,params))
                                
                                if df.empty:
                                    st.warning("Aucune donnée disponible pour ce moment.")
                                    st.stop()
                                else:
                                    
                                    colonnes_supplementaires = ["PARTIES", "ADVERSAIRES", "RESULTATS"]
                                    if all(col in df.columns for col in colonnes_supplementaires):
                                        # Suppression des autres parties pour un affiche plus aéré
                                        df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                                        # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                                        df_p = df.explode("PARTIES").reset_index(drop=True)
                                        df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                                        df_r = df.explode("RESULTATS").reset_index(drop=True)
                                        
                                        #transition
                                        adversaires_propres = df_a["ADVERSAIRES"][df_a["ADVERSAIRES"].apply(lambda x: isinstance(x, dict))]
                                        resultats_propres = df_r["RESULTATS"][df_r["RESULTATS"].apply(lambda x: isinstance(x, dict))]
                                                                            
                                        # Applatissement des colonnes imbriquées pour l'affichage
                                        parties_details = pd.json_normalize(df_p["PARTIES"])
                                        adversaires_details = pd.json_normalize(adversaires_propres)
                                        resultats_details = pd.json_normalize(resultats_propres)
                    
                                        # Renommage des colonnes pour une meilleure lisibilité
                                        df_l = df_l.rename(
                                            columns={
                                                "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                                "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                                "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                                "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                                "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                                "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                                "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                                "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                                "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                                
                                                "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                                "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                                
                                                "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                                
                                                # Tournoi
                                                "TOURNOI.ID": "ID Tournoi",
                                                "TOURNOI.NOM": "Nom du Tournoi", 
                                                "TOURNOI.TYPE": "Type du Tournoi", 
                                                "TOURNOI.PAYS": "Pays du Tournoi", 
                                                "TOURNOI.REGION": "Région du Tournoi", 
                                                "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                                "TOURNOI.TIER": "Tier du Tournoi", 
                                                "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                                "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                                "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                                "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                                "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                                "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                                "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                                "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                                "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                                
                                                # Ligue
                                                "LIGUE.ID": "ID Ligue",
                                                "LIGUE.NOM": "Nom de la Ligue",
                                                "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                                "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                                
                                                # Série
                                                "SERIE.ID": "ID Série",
                                                "SERIE.NOM": "Nom de la Série",
                                                "SERIE.ANNEE": "Année de la Série",
                                                "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                                "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                                "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                                "SERIE.DATE DE FIN": "Date de fin de la Série",
                                                "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                                "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                                "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                            }
                                        )
                                        st.write(f"Données récupérées pour {videogame} avec succès !")
                                        st.dataframe(df_l)  
                                        if "PARTIES" in df.columns:
                                            st.write("Données des parties :")
                                            st.dataframe(parties_details)
                                        if "ADVERSAIRES" in df.columns:
                                            st.write("Données des adversaires :")
                                            st.dataframe(adversaires_details)
                                        if "RESULTATS" in df.columns:
                                            st.write("Données des résultats des matchs :")
                                            st.dataframe(resultats_details) 
                                    
                                        st.write("Données brutes :")
                                        st.json(api_response)
                                    
                                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint,params), indent=4),file_name=filename,mime="application/json"):
                                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                    
                    
                if moments == "Annulé":
                    
                    endpoint = f"/{cat}/cancel"
                    filename = f"matchs_cancel.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        if df.empty:
                            st.warning("Aucune donnée disponible pour les matchs annulés.")
                            st.stop()
                        else:
                            # Suppression des autres parties pour un affiche plus aéré
                            df_l = df.drop(columns=["PARTIES", "ADVERSAIRES", "RESULTATS"])

                            # Séparation entre les dictionnaires et les listes de dictionnaires pour l'affichage des données tabulaires
                            df_p = df.explode("PARTIES").reset_index(drop=True)
                            df_a = df.explode("ADVERSAIRES").reset_index(drop=True)
                            df_r = df.explode("RESULTATS").reset_index(drop=True)
                            
                            # Applatissement des colonnes imbriquées pour l'affichage
                            parties_details = pd.json_normalize(df_p["PARTIES"])
                            adversaires_details = pd.json_normalize(df_a["ADVERSAIRES"])
                            resultats_details = pd.json_normalize(df_r["RESULTATS"])
                                                            
                            # Renommage des colonnes pour une meilleure lisibilité
                            df_l = df_l.rename(
                                columns={
                                    "DONNEES GENERALES DU MATCH.ID": "ID Match" ,
                                    "DONNEES GENERALES DU MATCH.NOM": "Nom du Match" ,
                                    "DONNEES GENERALES DU MATCH.JEU VIDEO": "Jeu Vidéo" ,
                                    "DONNEES GENERALES DU MATCH.VERSION ACTUELLE DU JEU": "Version du Jeu" ,
                                    "DONNEES GENERALES DU MATCH.STATUT": "Statut du Match" ,
                                    "DONNEES GENERALES DU MATCH.NOMBRE DE PARTIE": "Nombre de Parties" ,
                                    "DONNEES GENERALES DU MATCH.DATE DE DEBUT": "Date de Début" ,
                                    "DONNEES GENERALES DU MATCH.HEURE DE DEBUT": "Heure de Début" ,
                                    "DONNEES GENERALES DU MATCH.DATE DE FIN": "Date de Fin" ,
                                    "DONNEES GENERALES DU MATCH.HEURE DE FIN": "Heure de Fin" ,
                                    "DONNEES GENERALES DU MATCH.DATE DE MODIFICATION": "Date de Modification" ,
                                    "DONNEES GENERALES DU MATCH.HEURE DE MODIFICATION": "Heure de Modification" ,
                                    "DONNEES GENERALES DU MATCH.STATS DETAILLEES": "Stats Détaillées" ,
                                    
                                    "DONNEES GENERALES DU MATCH.LIVE.SUPPORT": "Live Supporté" ,
                                    "DONNEES GENERALES DU MATCH.LIVE.OUVERTURE": "Info Ouverture" ,
                                    
                                    "DONNEES GENERALES DU MATCH.AVANTAGE DURANT LA PARTIE": "Avantage lors de la partie" ,
                                    
                                    # Tournoi
                                    "TOURNOI.ID": "ID Tournoi",
                                    "TOURNOI.NOM": "Nom du Tournoi", 
                                    "TOURNOI.TYPE": "Type du Tournoi", 
                                    "TOURNOI.PAYS": "Pays du Tournoi", 
                                    "TOURNOI.REGION": "Région du Tournoi", 
                                    "TOURNOI.CASH PRIZE": "Cash Prize du Tournoi", 
                                    "TOURNOI.TIER": "Tier du Tournoi", 
                                    "TOURNOI.VAINQUEUR": "Vainqueur du Tournoi", 
                                    "TOURNOI.DATE DE DEBUT": "Date de Début du Tournoi" ,
                                    "TOURNOI.HEURE DE DEBUT": "Heure de Début du Tournoi" ,
                                    "TOURNOI.DATE DE FIN": "Date de Fin du Tournoi" ,
                                    "TOURNOI.HEURE DE FIN": "Heure de Fin du Tournoi" ,
                                    "TOURNOI.DATE DE MODIFICATION": "Date de Modification du Tournoi" ,
                                    "TOURNOI.HEURE DE MODIFICATION": "Heure de Modification du Tournoi" ,
                                    "TOURNOI.STATS DETAILLEES": "Stats Détaillées du Tournoi", 
                                    "TOURNOI.LIVE SUPPORT": "Live Supporté du Tournoi", 
                                    
                                    # Ligue
                                    "LIGUE.ID": "ID Ligue",
                                    "LIGUE.NOM": "Nom de la Ligue",
                                    "LIGUE.DATE DE MODIFICATION": "Date dernière modification Ligue",
                                    "LIGUE.HEURE DE MODIFICATION": "Heure dernière modification Ligue",
                                    
                                    # Série
                                    "SERIE.ID": "ID Série",
                                    "SERIE.NOM": "Nom de la Série",
                                    "SERIE.ANNEE": "Année de la Série",
                                    "SERIE.VAINQUEUR": "Vainqueur de la Série",
                                    "SERIE.DATE DE DEBUT": "Date de début de la Série",
                                    "SERIE.HEURE DE DEBUT": "Heure de début de la Série",
                                    "SERIE.DATE DE FIN": "Date de fin de la Série",
                                    "SERIE.HEURE DE FIN": "Heure de fin de la Série",
                                    "SERIE.DATE DE MODIFICATION": "Date de Modification de la Série",
                                    "SERIE.HEURE DE MODIFICATION": "Heure de Modification de la Série",

                                }
                            )
                        
                        
                        st.write(f"Données récupérées pour les matchs annumlés avec succès !")
                        st.dataframe(df_l)
                        st.write("Données des parties :")
                        st.dataframe(parties_details)
                        st.write("Données des adversaires :")
                        st.dataframe(adversaires_details)
                        st.write("Données des résultats des matchs :")
                        st.dataframe(resultats_details)
                        
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                        
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                                