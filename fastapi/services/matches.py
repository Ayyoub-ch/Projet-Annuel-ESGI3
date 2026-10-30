import json
from datetime import date
from pathlib import Path
from typing import Any

# Le chemin est calculé depuis ce fichier, pas depuis le dossier de lancement d'Uvicorn.
MATCHES_FOLDER = (
    Path(__file__).resolve().parents[2]
    / "data_recolt"
    / "data"
    / "matchs_data"
)
# TROUVER UNE SOLUTION POUR LES DATES DE FIN ET POUT LORSQUE TIME VAUT AUTRE CHOSE QUE PAST
def get_matches_by_time_period(
    time: str,
    videogame_name: str,
    date1: date,
    date2: date,
) -> list[dict[str, Any]]:
    """Renvoie les matchs du jeu dont la série est entièrement dans la période et du temps."""
    game_folder = (MATCHES_FOLDER / time / videogame_name).resolve()

    # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des matchs.
    try:
        game_folder.relative_to(MATCHES_FOLDER.resolve())
    except ValueError:
        raise FileNotFoundError("Jeu introuvable")

    if not game_folder.is_dir():
        raise FileNotFoundError("Jeu introuvable")

    matching_matches = []

    # Chaque match est stocké dans son propre dossier avec un fichier JSON.
    for match_path in sorted(game_folder.glob("*/*.json")):
        with match_path.open(encoding="utf-8") as file:
            match_data = json.load(file)
            
        matches_data = match_data["DONNEES GENERALES DU MATCH"]
        matches_start = date.fromisoformat(matches_data["DATE DE DEBUT"])
        matches_end = date.fromisoformat(matches_data["DATE DE FIN"])
        
        if date1 <= matches_start and matches_end <= date2:
            matching_matches.append(match_data)
            
        return matching_matches

def get_matches_by_time(
    time: str,
    videogame_name: str
) -> list[dict[str, Any]]:
    """Renvoie les matchs du jeu dont la série est entièrement dans la période."""
    game_folder = (MATCHES_FOLDER / time / videogame_name).resolve()

    # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des matchs.
    try:
        game_folder.relative_to(MATCHES_FOLDER.resolve())
    except ValueError:
        raise FileNotFoundError("Jeu introuvable")

    if not game_folder.is_dir():
        raise FileNotFoundError("Jeu introuvable")

    matching_matches = []

    # Chaque match est stocké dans son propre dossier avec un fichier JSON.
    for match_path in sorted(game_folder.glob("*/*.json")):
        with match_path.open(encoding="utf-8") as file:
            match_data = json.load(file)

        matching_matches.append(match_data)

    return matching_matches


def get_matches_by_period(
    videogame_name: str,
    date1: date,
    date2: date,
) -> list[dict[str, Any]]:
    """Renvoie les matchs du jeu dont la série est entièrement dans la période."""
    for category_folder in MATCHES_FOLDER.iterdir():
        game_folder = (category_folder / videogame_name).resolve()

        # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des matchs.
        try:
            game_folder.relative_to(MATCHES_FOLDER.resolve())
        except ValueError:
            raise FileNotFoundError("Jeu introuvable")

        if not game_folder.is_dir():
            raise FileNotFoundError("Jeu introuvable")

        matching_matches = []

        # Chaque match est stocké dans son propre dossier avec un fichier JSON.
        for match_path in sorted(game_folder.glob("*/*.json")):
            with match_path.open(encoding="utf-8") as file:
                match_data = json.load(file)

            matches_data = match_data["DONNEES GENERALES DU MATCH"]
            matches_start = date.fromisoformat(matches_data["DATE DE DEBUT"])
            matches_end = date.fromisoformat(matches_data["DATE DE FIN"])

            # Le tournoi doit commencer après date1 et finir avant date2 (bornes incluses).
            if date1 <= matches_start and matches_end <= date2:
                matching_matches.append(match_data)

    return matching_matches


def get_matches_by_date(
    videogame_name: str,
    date1: date
) -> list[dict[str, Any]]:
    """Renvoie les matchs du jeu dont la date de début du tournoi est entièrement dans la date."""
    # Parcourt toutes les catégories pour trouver le jeu sans demander la catégorie.
    for category_folder in MATCHES_FOLDER.iterdir():
        game_folder = (category_folder / videogame_name).resolve()

        # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des matchs.
        try:
            game_folder.relative_to(MATCHES_FOLDER.resolve())
        except ValueError:
            raise FileNotFoundError("Jeu introuvable")

        if not game_folder.is_dir():
            raise FileNotFoundError("Jeu introuvable")

        matching_matches = []

        # Chaque match est stocké dans son propre dossier avec un fichier JSON.
        for match_path in sorted(game_folder.glob("*/*.json")):
            with match_path.open(encoding="utf-8") as file:
                match_data = json.load(file)

            matches_data = match_data["DONNEES GENERALES DU MATCH"]
            matches_start = date.fromisoformat(matches_data["DATE DE DEBUT"])

            # La série doit commencer après date1 et finir avant date2 (bornes incluses).
            if date1 == matches_start:
                matching_matches.append(matches_data)

    return matching_matches


def get_matches_by_now(
    videogame_name: str
) -> list[dict[str, Any]]:
    """Renvoie les matchs du jeu dont la date de début du tournoi est entièrement dans la date."""
    game_folder = (MATCHES_FOLDER / "running" /videogame_name).resolve()

    # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des matchs.
    try:
        game_folder.relative_to(MATCHES_FOLDER.resolve())
    except ValueError:
        raise FileNotFoundError("Jeu introuvable")

    if not game_folder.is_dir():
        raise FileNotFoundError("Jeu introuvable")

    matching_matches = []

    # Chaque match est stocké dans son propre dossier avec un fichier JSON.
    for match_path in sorted(game_folder.glob("*/*.json")):
        with match_path.open(encoding="utf-8") as file:
            match_data = json.load(file)

        matches_data = match_data["DONNEES GENERALES DU MATCH"]
        matches_start = date.fromisoformat(matches_data["DATE DE DEBUT"])

        # Le tournoi doit commencer après date1 et finir avant date2 (bornes incluses).
        if matches_start <= date.today() :
            matching_matches.append(match_data)

    return matching_matches