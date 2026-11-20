
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
    # STOP
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
DOSSIER_PRINCIPAL = "data/football/teams_data"



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
    if c ==100:
        break
    try:

        response = requests.get(url_api, headers=headers, timeout=600)
        response.raise_for_status()  # Lève une erreur si problème réseau
        
        # Conversion de la réponse en JSON Python
        reponse_json = response.json()
        teams_data = reponse_json.get("response", [])
        print(f" {len(teams_data)} equipes recuperees depuis l'API")
        
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
    nom_stade= stade.get("name").replace("/", "_").replace(":", "_").replace(" ", "_").replace("\u0131", "i")
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




