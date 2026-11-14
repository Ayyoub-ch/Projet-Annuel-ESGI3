import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.matches import get_matches_by_time


router = APIRouter(prefix="/match", tags=["match"])


@router.get("/{videogame_name}/time")
def download_matches_by_time(
    videogame_name: str,
    time: str
    ):
    """Renvoie toutes les matchs issues du temps demandé.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    \nTime : choisir entre upcoming, past et running pour avoir les matchs récents, passés et en cours"""
    try:
        matches = get_matches_by_time(time, videogame_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"matchs_{videogame_name}_{time}.json"

    return Response(
        content=json.dumps(matches, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
