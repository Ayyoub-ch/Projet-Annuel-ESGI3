import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.leagues import get_leagues_by_date


router = APIRouter(prefix="/league", tags=["league"])


@router.get("/{videogame_name}/date")
def download_leagues_by_date(
    videogame_name: str,
    date1: date
    ):
    """Renvoie toutes les ligues du jeu comprises dans la date demandée.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    \nDate au format : YYYY-MM-DD"""
    date_now = date.today()
    if date1 > date_now:
        raise HTTPException(
            status_code=422,
            detail="date1 doit être antérieure ou égale à la date d'aujourd'hui",
        )

    try:
        leagues = get_leagues_by_date(videogame_name, date1)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"ligues_{videogame_name}_{date1:%Y-%m-%d}.json"

    return Response(
        content=json.dumps(leagues, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
