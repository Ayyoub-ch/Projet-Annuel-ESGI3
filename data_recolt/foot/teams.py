
# ================================
# IMPORT DES BIBLIOTHÈQUES
# ================================
import requests    # Pour récupérer les données depuis l'API
import os          # Pour créer des dossiers et gérer les fichiers
import json        # Pour manipuler et sauvegarder les fichiers JSON

# ================================
# CONFIGURATION DES DOSSIERS
# ================================




countries = [
    "albania",
    "algeria",
    "andorra",
    "angola",
    "antigua-and-barbuda",
    "argentina",
    "armenia",
    "aruba",
    "australia",
    "austria",
    "azerbaijan",
    "bahrain",
    "bangladesh",
    "barbados",
    "belarus",
    "belgium",
    "belize",
    "benin",
    "bermuda",
    "bhutan",
    "bolivia",
    "bosnia",
    "botswana",
    "brazil",
    "bulgaria",
    "burkina-faso",
    "burundi",
    "cambodia",
    "cameroon",
    "canada",
    "chile",
    "china",
    "chinese-taipei",
    "colombia",
    "congo",
    "congo-dr",
    "costa-rica",
    "crimea",
    "croatia",
    "cuba",
    "curacao",
    "cyprus",
    "czech-republic",
    "denmark",
    "dominican-republic",
    "ecuador",
    "egypt",
    "el-salvador",
    "england",
    "estonia",
    "eswatini",
    "ethiopia",
    "faroe-islands",
    "fiji",
    "finland",
    "france",
    "gabon",
    "gambia",
    "georgia",
    "germany",
    "ghana",
    "gibraltar",
    "greece",
    "grenada",
    "guadeloupe",
    "guatemala",
    "guinea",
    "haiti",
    "honduras",
    "hong-kong",
    "hungary",
    "iceland",
    "india",
    "indonesia",
    "iran",
    "iraq",
    "ireland",
    "israel",
    "italy",
    "ivory-coast",
    "jamaica",
    "japan",
    "jordan",
    "kazakhstan",
    "kenya",
    "kosovo",
    "kuwait",
    "kyrgyzstan",
    "laos",
    "latvia",
    "lebanon",
    "lesotho",
    "liberia",
    "libya",
    "liechtenstein",
    "lithuania",
    "luxembourg",
    "macau",
    "macedonia",
    "malawi",
    "malaysia",
    "maldives",
    "mali",
    "malta",
    "mauritania",
    "mauritius",
    "mexico",
    "moldova",
    "mongolia",
    "montenegro",
    "morocco",
    "myanmar",
    "namibia",
    "nepal",
    "netherlands",
    "new-zealand",
    "nicaragua",
    "nigeria",
    "northern-ireland",
    "norway",
    "oman",
    "pakistan",
    "palestine",
    "panama",
    "paraguay",
    "peru",
    "philippines",
    "poland",
    "portugal",
    "qatar",
    "romania",
    "russia",
    "rwanda",
    "san-marino",
    "saudi-arabia",
    "scotland",
    "senegal",
    "serbia",
    "singapore",
    "slovakia",
    "slovenia",
    "somalia",
    "south-africa",
    "south-korea",
    "spain",
    "sudan",
    "suriname",
    "sweden",
    "switzerland",
    "syria",
    "tajikistan",
    "tanzania",
    "thailand",
    "togo",
    "trinidad-and-tobago",
    "tunisia",
    "turkey",
    "turkmenistan",
    "uganda",
    "ukraine",
    "united-arab-emirates",
    "uruguay",
    "usa",
    "uzbekistan",
    "venezuela",
    "vietnam",
    "wales",
    "world",
    "yemen",
    "zambia",
    "zimbabwe"
]


# Dossier principal
DOSSIER_PRINCIPAL = "data/football/leagues_data"



# ================================
# URL DE L'API JSON
# ================================
for country in countries:
    url_api= f"https://v3.football.api-sports.io/teams?country={country}"

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
        teams_data = reponse_json.get("response", [])
        print(f" {len(teams_data)} ligues récupérées depuis l'API")
        
    except requests.exceptions.RequestException as e:
        print(f" Erreur lors de la recuperation des donnees depuis l'API: {e}")
        exit(1)  # Quitte le script avec un code d'erreur
        
# ================================
# TRAITEMENT DE CHAQUE LIGUE
# ================================ 






