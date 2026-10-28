import json
from datetime import date
from pathlib import Path
from typing import Any

# Le chemin est calculé depuis ce fichier, pas depuis le dossier de lancement d'Uvicorn.
TOURNAMENTS_FOLDER = (
    Path(__file__).resolve().parents[2]
    / "data_recolt"
    / "data"
    / "tournaments_data"
)


def get_tournaments_by_period(
    videogame_name: str,
    date1: date,
    date2: date,
) -> list[dict[str, Any]]:
    """Renvoie les tournois du jeu dont la série est entièrement dans la période."""
    game_folder = (TOURNAMENTS_FOLDER / videogame_name).resolve()

    # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des tournois.
    try:
        game_folder.relative_to(TOURNAMENTS_FOLDER.resolve())
    except ValueError:
        raise FileNotFoundError("Jeu introuvable")

    if not game_folder.is_dir():
        raise FileNotFoundError("Jeu introuvable")

    matching_tournaments = []

    # Chaque tournoi est stocké dans son propre dossier avec un fichier JSON.
    for tournament_path in sorted(game_folder.glob("*/*.json")):
        with tournament_path.open(encoding="utf-8") as file:
            tournament_data = json.load(file)

        tournaments_data = tournament_data["DONNEES GENERALES DU TOURNOIS"]
        tournaments_start = date.fromisoformat(tournaments_data["DATE DE DEBUT"])
        tournaments_end = date.fromisoformat(tournaments_data["DATE DE FIN"])

        # Le tournoi doit commencer après date1 et finir avant date2 (bornes incluses).
        if date1 <= tournaments_start and tournaments_end <= date2:
            matching_tournaments.append(tournament_data)

    return matching_tournaments


def get_tournaments_by_date(
    videogame_name: str,
    date1: date
) -> list[dict[str, Any]]:
    """Renvoie les tournois du jeu dont la date de début du tournoi est entièrement dans la date."""
    game_folder = (TOURNAMENTS_FOLDER / videogame_name).resolve()

    # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des tournois.
    try:
        game_folder.relative_to(TOURNAMENTS_FOLDER.resolve())
    except ValueError:
        raise FileNotFoundError("Jeu introuvable")

    if not game_folder.is_dir():
        raise FileNotFoundError("Jeu introuvable")

    matching_tournaments = []

    # Chaque tournoi est stocké dans son propre dossier avec un fichier JSON.
    for tournament_path in sorted(game_folder.glob("*/*.json")):
        with tournament_path.open(encoding="utf-8") as file:
            tournament_data = json.load(file)

        tournaments_data = tournament_data["DONNEES GENERALES DU TOURNOIS"]
        tournaments_start = date.fromisoformat(tournaments_data["DATE DE DEBUT"])

        # La série doit commencer après date1 et finir avant date2 (bornes incluses).
        if date1 == tournaments_start:
            matching_tournaments.append(tournaments_data)

    return matching_tournaments


def get_tournaments_by_now(
    videogame_name: str
) -> list[dict[str, Any]]:
    """Renvoie les tournois du jeu dont la date de début du tournoi est entièrement dans la date."""
    game_folder = (TOURNAMENTS_FOLDER / videogame_name).resolve()

    # Empêche qu'un nom de jeu reçu dans l'URL sorte du dossier des tournois.
    try:
        game_folder.relative_to(TOURNAMENTS_FOLDER.resolve())
    except ValueError:
        raise FileNotFoundError("Jeu introuvable")

    if not game_folder.is_dir():
        raise FileNotFoundError("Jeu introuvable")

    matching_tournaments = []

    # Chaque tournoi est stocké dans son propre dossier avec un fichier JSON.
    for tournament_path in sorted(game_folder.glob("*/*.json")):
        with tournament_path.open(encoding="utf-8") as file:
            tournament_data = json.load(file)

        tournaments_data = tournament_data["DONNEES GENERALES DU TOURNOIS"]
        tournaments_start = date.fromisoformat(tournaments_data["DATE DE DEBUT"])
        tournaments_end = date.fromisoformat(tournaments_data["DATE DE FIN"])

        # Le tournoi doit commencer après date1 et finir avant date2 (bornes incluses).
        if tournaments_start <= date.today() <= tournaments_end:
            matching_tournaments.append(tournament_data)

    return matching_tournaments