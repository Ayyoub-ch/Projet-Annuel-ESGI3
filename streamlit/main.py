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

API_ESPORT = f"{BASE_URL}/esport"


# ========================================
# VARIABLES POUR API E-SPORT
# ========================================

ESPORT_TYPES = ["ligues", "series", "tournois","matchs" ]
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
is_connected_esport, api_response_esport = check_api_connection(API_ESPORT)

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
    if category == "ligues" :
        st.header("Ligues")
        st.markdown("Récupère les données des ligues E-Sport. ")
        
        # Variables par défaut
        endpoint = None
        params = None
        filename = None
        
        moments = st.selectbox("Moment :", moments_esport_classic)
        
        if moments == "Maintenant":
            
            videogame = st.selectbox("Jeu Vidéo :", jeux)
            
            if videogame == "Call of Duty":
                endpoint = f"/{videogame}/now"
                filename = "ligues_{videogame}_now.json"