import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.matches import get_matches_by_time_period


router = APIRouter(prefix="/match", tags=["match"])


@router.get("/{videogame_name}/time_period")
def download_matches_by_time_period(
    time: str,
    videogame_name: str,
    date1: date,
    date2: date
    ):
    """Renvoie toutes les matchs du jeu comprises dans la date demandée.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    \nTime : choisir entre upcoming, past et running pour avoir les matchs récents, passés et en cours"""
    if date1 > date2:
            raise HTTPException(
                status_code=422,
                detail="date1 doit être antérieure ou égale à date2",
            )
    try:
        matches = get_matches_by_time_period(time, videogame_name, date1, date2)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"matchs_{videogame_name}_{time}_{date1:%Y-%m-%d}_{date2:%Y-%m-%d}.json"

    return Response(
        content=json.dumps(matches, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
