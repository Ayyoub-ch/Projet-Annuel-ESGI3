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
BASE_URL = "http://127.0.0.1:8000"

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
        "Mobile Legends : Bang Bang", "Rainbow 6 Siege", "Starcraft 2", "Valorant"]


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
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                    df = pd.json_normalize(fetch_data(endpoint))
                    st.write("Données récupérées pour Counter Strike avec succès !")
                    st.dataframe(df)
                    st.write("Données brutes :")
                    st.json(fetch_data(endpoint))
                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")

            
            elif videogame == "Counter Strike":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                    df = pd.json_normalize(fetch_data(endpoint))
                    st.write("Données récupérées pour Counter Strike avec succès !")
                    st.dataframe(df)
                    st.write("Données brutes :")
                    st.json(fetch_data(endpoint))
                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")
                

            elif videogame == "Dota 2":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                    df = pd.json_normalize(fetch_data(endpoint))
                    st.write("Données récupérées pour Dota 2 avec succès !")
                    st.dataframe(df)
                    st.write("Données brutes :")
                    st.json(fetch_data(endpoint))
                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")


            elif videogame == "King of Glory":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                    df = pd.json_normalize(fetch_data(endpoint))
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
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                    df = pd.json_normalize(fetch_data(endpoint))
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
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                    df = pd.json_normalize(fetch_data(endpoint))
                    st.write("Données récupérées pour Mobile Legends : Bang Bang avec succès !")
                    st.dataframe(df)
                    st.write("Données brutes :")
                    st.json(fetch_data(endpoint))
                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")

                
            elif videogame == "Rainbow 6 Siege":
                endpoint = f"/{cat}/{videogame}/now"
                filename = f"ligues_{videogame}_now.json"
                
                if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                    df = pd.json_normalize(fetch_data(endpoint))
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
                    df = pd.json_normalize(fetch_data(endpoint))
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
                    df = pd.json_normalize(fetch_data(endpoint))
                    st.write("Données récupérées pour Valorant avec succès !")
                    st.dataframe(df)
                    st.write("Données brutes :")
                    st.json(fetch_data(endpoint))
                if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                    st.success(f"Les données ont été téléchargées sous le nom {filename}.")


        # mettre le tableau en DF
        
        if moments == "Par Période":
            
            videogame = st.selectbox("Jeu Vidéo :", jeux)
            
            if videogame == "Call of Duty":
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"

            elif videogame == "Counter Strike":
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"

            elif videogame == "Dota 2":
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
            elif videogame == "King of Glory":
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
            
            elif videogame == "League of Legends":
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
            
            elif videogame == "Mobile Legends : Bang Bang":
                videogame = "Mobile Legends Bang Bang"
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
            elif videogame == "Rainbow 6 Siege":
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
            
            elif videogame == "Starcraft 2":
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"
                
            elif videogame == "Valorant":
                endpoint = f"/{cat}/{videogame}/period"
                filename = f"ligues_{videogame}_period.json"


        if moments == "Par Date":
            
            videogame = st.selectbox("Jeu Vidéo :", jeux)
            
            if videogame == "Call of Duty":
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
            elif videogame == "Counter Strike":
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                        
            elif videogame == "Dota 2":
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
            elif videogame == "King of Glory":
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
            
            elif videogame == "League of Legends":
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
            
            elif videogame == "Mobile Legends : Bang Bang":
                videogame = "Mobile Legends Bang Bang"
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
            elif videogame == "Rainbow 6 Siege":
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
            
            elif videogame == "Starcraft 2":
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
            elif videogame == "Valorant":
                endpoint = f"/{cat}/{videogame}/date"
                filename = f"ligues_{videogame}_date.json"
                
                
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
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        st.write("Données récupérées pour Call of Duty avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
                elif videogame == "Counter Strike":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        st.write("Données récupérées pour Counter Strike avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                            
                elif videogame == "Dota 2":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        st.write("Données récupérées pour Dota 2 avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
                elif videogame == "King of Glory":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        st.write("Données récupérées pour King of Glory avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                
                elif videogame == "League of Legends":
                    videogame = "LoL"
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        st.write("Données récupérées pour League of Legends avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                
                elif videogame == "Mobile Legends : Bang Bang":
                    videogame = "Mobile Legends Bang Bang"
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        st.write("Données récupérées pour Mobile Legends : Bang Bang avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
                elif videogame == "Rainbow 6 Siege":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        st.write("Données récupérées pour Rainbow 6 Siege avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                
                elif videogame == "Starcraft 2":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        st.write("Données récupérées pour Starcraft 2 avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
                elif videogame == "Valorant":
                    endpoint = f"/{cat}/{videogame}/now"
                    filename = f"series_{videogame}_now.json"
                    
                    if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                        df = pd.json_normalize(fetch_data(endpoint))
                        st.write("Données récupérées pour Valorant avec succès !")
                        st.dataframe(df)
                        st.write("Données brutes :")
                        st.json(fetch_data(endpoint))
                    if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                        st.success(f"Les données ont été téléchargées sous le nom {filename}.")
    
                    
            if moments == "Période":
                
                videogame = st.selectbox("Jeu Vidéo :", jeux)
            
                if videogame == "Call of Duty":
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                        
                elif videogame == "Counter Strike":
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                            
                elif videogame == "Dota 2":
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                elif videogame == "King of Glory":
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                
                elif videogame == "League of Legends":
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                
                elif videogame == "Mobile Legends : Bang Bang":
                    videogame = "Mobile Legends Bang Bang"
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                elif videogame == "Rainbow 6 Siege":
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                
                elif videogame == "Starcraft 2":
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"
                    
                elif videogame == "Valorant":
                    endpoint = f"/{cat}/{videogame}/period"
                    filename = f"series_{videogame}_period.json"       
                      
    
            if moments == "Date":
                            
                videogame = st.selectbox("Jeu Vidéo :", jeux)
            
                if videogame == "Call of Duty":
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                        
                elif videogame == "Counter Strike":
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                            
                elif videogame == "Dota 2":
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                elif videogame == "King of Glory":
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                
                elif videogame == "League of Legends":
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                
                elif videogame == "Mobile Legends : Bang Bang":
                    videogame = "Mobile Legends Bang Bang"
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                elif videogame == "Rainbow 6 Siege":
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                
                elif videogame == "Starcraft 2":
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"
                    
                elif videogame == "Valorant":
                    endpoint = f"/{cat}/{videogame}/date"
                    filename = f"series_{videogame}_date.json"   
                    
                    
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
                            if not df.empty:
                                # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                                df["EQUIPES"] = df["EQUIPES"].apply(extract_name)
                                df["MEMBRES DE L'EQUIPE"] = df["MEMBRES DE L'EQUIPE"].apply(extract_name)
                                df["MATCHES"] = df["MATCHES"].apply(extract_name)
                                
                                df = df.rename(
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
                                    # Listes imbriquées et autres objets
                                    "MATCHES": "Matchs",
                                    "EQUIPES": "Équipes",
                                    "MEMBRES DE L'EQUIPE": "Membres de l'équipe",
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
                            
                            
                            
                            st.write("Données récupérées pour Call of Duty avec succès !")
                            st.dataframe(df)
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                            
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                        
                    elif videogame == "Counter Strike":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if not df.empty:
                                # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                                df["EQUIPES"] = df["EQUIPES"].apply(extract_name)
                                df["MEMBRES DE L'EQUIPE"] = df["MEMBRES DE L'EQUIPE"].apply(extract_name)
                                df["MATCHES"] = df["MATCHES"].apply(extract_name)
                                
                                df = df.rename(
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
                                    # Listes imbriquées et autres objets
                                    "MATCHES": "Matchs",
                                    "EQUIPES": "Équipes",
                                    "MEMBRES DE L'EQUIPE": "Membres de l'équipe",
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
                            st.dataframe(df)
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                            
                    elif videogame == "Dota 2":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if not df.empty:
                            # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                                df["EQUIPES"] = df["EQUIPES"].apply(extract_name)
                                df["MEMBRES DE L'EQUIPE"] = df["MEMBRES DE L'EQUIPE"].apply(extract_name)
                                df["MATCHES"] = df["MATCHES"].apply(extract_name)
                                
                                df = df.rename(
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
                                    # Listes imbriquées et autres objets
                                    "MATCHES": "Matchs",
                                    "EQUIPES": "Équipes",
                                    "MEMBRES DE L'EQUIPE": "Membres de l'équipe",
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
                            
                            st.write("Données récupérées pour Dota 2 avec succès !")
                            st.dataframe(df)
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                        
                    elif videogame == "King of Glory":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if not df.empty:
                            # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                                df["EQUIPES"] = df["EQUIPES"].apply(extract_name)
                                df["MEMBRES DE L'EQUIPE"] = df["MEMBRES DE L'EQUIPE"].apply(extract_name)
                                df["MATCHES"] = df["MATCHES"].apply(extract_name)
                                
                                df = df.rename(
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
                                    # Listes imbriquées et autres objets
                                    "MATCHES": "Matchs",
                                    "EQUIPES": "Équipes",
                                    "MEMBRES DE L'EQUIPE": "Membres de l'équipe",
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
                            st.write("Données récupérées pour King of Glory avec succès !")
                            st.dataframe(df)
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                    
                    elif videogame == "League of Legends":
                        videogame = "LoL"
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if not df.empty:
                                # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                                df["EQUIPES"] = df["EQUIPES"].apply(extract_name)
                                df["MEMBRES DE L'EQUIPE"] = df["MEMBRES DE L'EQUIPE"].apply(extract_name)
                                df["MATCHES"] = df["MATCHES"].apply(extract_name)
                                
                                df = df.rename(
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
                                    # Listes imbriquées et autres objets
                                    "MATCHES": "Matchs",
                                    "EQUIPES": "Équipes",
                                    "MEMBRES DE L'EQUIPE": "Membres de l'équipe",
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
                            st.dataframe(df)
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
                            
                            if not df.empty:
                                # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                                df["EQUIPES"] = df["EQUIPES"].apply(extract_name)
                                df["MEMBRES DE L'EQUIPE"] = df["MEMBRES DE L'EQUIPE"].apply(extract_name)
                                df["MATCHES"] = df["MATCHES"].apply(extract_name)
                                
                                df = df.rename(
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
                                    # Listes imbriquées et autres objets
                                    "MATCHES": "Matchs",
                                    "EQUIPES": "Équipes",
                                    "MEMBRES DE L'EQUIPE": "Membres de l'équipe",
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
                            
                            st.write("Données récupérées pour Mobile Legends Bang Bang avec succès !")
                            st.dataframe(df)
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                        
                    elif videogame == "Rainbow 6 Siege":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            if not df.empty:
                                # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                                df["EQUIPES"] = df["EQUIPES"].apply(extract_name)
                                df["MEMBRES DE L'EQUIPE"] = df["MEMBRES DE L'EQUIPE"].apply(extract_name)
                                df["MATCHES"] = df["MATCHES"].apply(extract_name)
                                
                                df = df.rename(
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
                                    # Listes imbriquées et autres objets
                                    "MATCHES": "Matchs",
                                    "EQUIPES": "Équipes",
                                    "MEMBRES DE L'EQUIPE": "Membres de l'équipe",
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
                            
                            st.write("Données récupérées pour Rainbow 6 Siege avec succès !")
                            st.dataframe(df)
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                    
                    elif videogame == "Starcraft 2":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if not df.empty:
                                # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                                df["EQUIPES"] = df["EQUIPES"].apply(extract_name)
                                df["MEMBRES DE L'EQUIPE"] = df["MEMBRES DE L'EQUIPE"].apply(extract_name)
                                df["MATCHES"] = df["MATCHES"].apply(extract_name)
                                
                                df = df.rename(
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
                                    # Listes imbriquées et autres objets
                                    "MATCHES": "Matchs",
                                    "EQUIPES": "Équipes",
                                    "MEMBRES DE L'EQUIPE": "Membres de l'équipe",
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
                            st.write("Données récupérées pour Starcraft 2 avec succès !")
                            st.dataframe(df)
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        
                        
                    elif videogame == "Valorant":
                        endpoint = f"/{cat}/{videogame}/now"
                        filename = f"tournois_{videogame}_now.json"
                        
                        if st.button("Récupérer les données", on_click=fetch_data, args=(endpoint,)):
                            df = pd.json_normalize(fetch_data(endpoint))
                            
                            if not df.empty:
                                # C'est ici que Pandas envoie chaque ligne une par une dans 'val' :
                                df["EQUIPES"] = df["EQUIPES"].apply(extract_name)
                                df["MEMBRES DE L'EQUIPE"] = df["MEMBRES DE L'EQUIPE"].apply(extract_name)
                                df["MATCHES"] = df["MATCHES"].apply(extract_name)
                                
                                df = df.rename(
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
                                    # Listes imbriquées et autres objets
                                    "MATCHES": "Matchs",
                                    "EQUIPES": "Équipes",
                                    "MEMBRES DE L'EQUIPE": "Membres de l'équipe",
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
                            st.write("Données récupérées pour Valorant avec succès !")
                            st.dataframe(df)
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
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
                            st.write("Données récupérées pour Call of Duty avec succès !")
                            st.dataframe(df)
                            st.write("Données brutes :")
                            st.json(fetch_data(endpoint))
                        if st.download_button(label="Télécharger les données",data=json.dumps(fetch_data(endpoint), indent=4),file_name=filename,mime="application/json"):
                            st.success(f"Les données ont été téléchargées sous le nom {filename}.")
        