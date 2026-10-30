import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.matches import get_matches_by_date


router = APIRouter(prefix="/match", tags=["match"])


@router.get("/{videogame_name}/date")
def download_matches_by_date(
    videogame_name: str,
    date1: date
    ):
    """Renvoie toutes les matchs du jeu comprises dans la date demandée.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    \nDate au format : YYYY-MM-DD"""
    try:
        matches = get_matches_by_date(videogame_name, date1)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"matchs_{videogame_name}_{date1:%Y-%m-%d}.json"

    return Response(
        content=json.dumps(matches, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
