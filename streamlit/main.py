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

API_ESPORT = f"{BASE_URL}/docs"

# ========================================
# APPEL DE L'API E-SPORT
# ========================================
def check_api_connection(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Vérifie si la requête a réussi (code 200)
        return True, response.json()  # Retourne True et les données JSON
    except requests.exceptions.RequestException as e:
        return False, str(e)  # Retourne False et le message d'erreur
# ========================================
# VARIABLES POUR API E-SPORT
# ========================================

ESPORT_TYPES = ["Ligues", "Series", "Tournois","Matchs" ]
moments_esport_classic = ["Maintenant", "Par Période", "Par Date"]
moments_esport_match = ["Maintenant", "Par Période", "Par Date", "Par Temps", "Annulé"]
jeux = ["Call of Duty", "Counter Strike", "Dota 2", "King of Glory", "League of Legends", 
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
                filename = "ligues_{videogame}_now.json"
            
            elif videogame == "Counter Strike":
                endpoint = f"/{cat}/{videogame}/now"
                filename = "ligues_{videogame}_now.json"
            
            elif videogame == "Dota 2":
                endpoint = f"/{cat}/{videogame}/now"
                filename = "ligues_{videogame}_now.json"
                
            elif videogame == "King of Glory":
                endpoint = f"/{cat}/{videogame}/now"
                filename = "ligues_{videogame}_now.json"
            
            elif videogame == "League of Legends":
                endpoint = f"/{cat}/{videogame}/now"
                filename = "ligues_{videogame}_now.json"
            
            elif videogame == "Mobile Legends : Bang Bang":
                videogame = "Mobile Legends Bang Bang"
                endpoint = f"/{cat}/{videogame}/now"
                filename = "ligues_{videogame}_now.json"
                
            elif videogame == "Rainbow 6 Siege":
                endpoint = f"/{cat}/{videogame}/now"
                filename = "ligues_{videogame}_now.json"
            
            elif videogame == "Starcraft 2":
                endpoint = f"/{cat}/{videogame}/now"
                filename = "ligues_{videogame}_now.json"
                
            elif videogame == "Valorant":
                endpoint = f"/{cat}/{videogame}/now"
                filename = "ligues_{videogame}_now.json"
                
            
                
        # mettre le tableau en DF
        
        if moments == "Par Période":
            
            videogame = st.selectbox("Jeu Vidéo :", jeux)
            
            if videogame == "Call of Duty":
                endpoint = f"/{cat}/{videogame}/period"
                filename = "ligues_{videogame}_period.json"
        
        if moments == "Par Date":
            
            videogame = st.selectbox("Jeu Vidéo :", jeux)
            
            if videogame == "Call of Duty":
                endpoint = f"/{cat}/{videogame}/date"
                filename = "ligues_{videogame}_date.json"
                
            elif videogame == "Counter Strike":
                endpoint = f"/{cat}/{videogame}/date"
                filename = "ligues_{videogame}_date.json"
                        
            elif videogame == "Dota 2":
                endpoint = f"/{cat}/{videogame}/date"
                filename = "ligues_{videogame}_date.json"
                
            elif videogame == "King of Glory":
                endpoint = f"/{cat}/{videogame}/date"
                filename = "ligues_{videogame}_date.json"
            
            elif videogame == "League of Legends":
                endpoint = f"/{cat}/{videogame}/date"
                filename = "ligues_{videogame}_date.json"
            
            elif videogame == "Mobile Legends : Bang Bang":
                videogame = "Mobile Legends Bang Bang"
                endpoint = f"/{cat}/{videogame}/date"
                filename = "ligues_{videogame}_date.json"
                
            elif videogame == "Rainbow 6 Siege":
                endpoint = f"/{cat}/{videogame}/date"
                filename = "ligues_{videogame}_date.json"
            
            elif videogame == "Starcraft 2":
                endpoint = f"/{cat}/{videogame}/date"
                filename = "ligues_{videogame}_date.json"
                
            elif videogame == "Valorant":
                endpoint = f"/{cat}/{videogame}/date"
                filename = "ligues_{videogame}_date.json"
                
                
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
                    filename = "series_{videogame}_now.json"
                    
    
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
                        filename = "tournois_{videogame}_now.json"
                        
                        
    
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
                        filename = "matchs_{videogame}_now.json"