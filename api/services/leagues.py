import json
from datetime import date
from pathlib import Path
from typing import Any

# Le chemin est calculé depuis ce fichier, pas depuis le dossier de lancement d'Uvicorn.
LEAGUES_FOLDER = (
    Path(__file__).resolve().parents[2]
    / "data_recolt"
    / "data"
    / "leagues_data"
)


def get_leagues_by_period(
    videogame_name: str,
    date1: date,
    date2: date,
) -> list[dict[str, Any]]:
    """Renvoie les ligues du jeu dont la série est entièrement dans la période."""
    game_folder = (LEAGUES_FOLDER / videogame_name).resolve()

    # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des ligues.
    try:
        game_folder.relative_to(LEAGUES_FOLDER.resolve())
    except ValueError:
        raise FileNotFoundError("Jeu introuvable")

    if not game_folder.is_dir():
        raise FileNotFoundError("Jeu introuvable")

    matching_leagues = []

    # Chaque ligue est stockée dans son propre dossier avec un fichier JSON.
    for league_path in sorted(game_folder.glob("*/*.json")):
        with league_path.open(encoding="utf-8") as file:
            league_data = json.load(file)

        series_data = league_data["SERIE"]
        series_start = date.fromisoformat(series_data["DATE DE DEBUT"])
        series_end = date.fromisoformat(series_data["DATE DE FIN"])

        # La série doit commencer après date1 et finir avant date2 (bornes incluses).
        if date1 <= series_start and series_end <= date2:
            matching_leagues.append(league_data)

    return matching_leagues


def get_leagues_by_date(
    videogame_name: str,
    date1: date
) -> list[dict[str, Any]]:
    """Renvoie les ligues du jeu dont la date de début de la série est entièrement dans la date."""
    game_folder = (LEAGUES_FOLDER / videogame_name).resolve()

    # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des ligues.
    try:
        game_folder.relative_to(LEAGUES_FOLDER.resolve())
    except ValueError:
        raise FileNotFoundError("Jeu introuvable")

    if not game_folder.is_dir():
        raise FileNotFoundError("Jeu introuvable")

    matching_leagues = []

    # Chaque ligue est stockée dans son propre dossier avec un fichier JSON.
    for league_path in sorted(game_folder.glob("*/*.json")):
        with league_path.open(encoding="utf-8") as file:
            league_data = json.load(file)

        series_data = league_data["SERIE"]
        series_start = date.fromisoformat(series_data["DATE DE DEBUT"])

        # La série doit commencer après date1 et finir avant date2 (bornes incluses).
        if date1 == series_start:
            matching_leagues.append(league_data)

    return matching_leagues


def get_leagues_by_now(
    videogame_name: str
) -> list[dict[str, Any]]:
    """Renvoie les ligues du jeu dont la date de début de la série est entièrement dans la date."""
    game_folder = (LEAGUES_FOLDER / videogame_name).resolve()

    # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des ligues.
    try:
        game_folder.relative_to(LEAGUES_FOLDER.resolve())
    except ValueError:
        raise FileNotFoundError("Jeu introuvable")

    if not game_folder.is_dir():
        raise FileNotFoundError("Jeu introuvable")

    matching_leagues = []

    # Chaque ligue est stockée dans son propre dossier avec un fichier JSON.
    for league_path in sorted(game_folder.glob("*/*.json")):
        with league_path.open(encoding="utf-8") as file:
            league_data = json.load(file)

        series_data = league_data["SERIE"]
        series_start = date.fromisoformat(series_data["DATE DE DEBUT"])
        series_end = date.fromisoformat(series_data["DATE DE FIN"])

        # La série doit commencer après date1 et finir avant date2 (bornes incluses).
        if series_start <= date.today() <= series_end:
            matching_leagues.append(league_data)

    return matching_leagues