import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.series import get_series_by_date


router = APIRouter(prefix="/serie", tags=["serie"])


@router.get("/{videogame_name}/date")
def download_series_by_date(
    videogame_name: str,
    date1: date
    ):
    """Renvoie toutes les series à la date demandée.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    \nDate au format : YYYY-MM-DD"""
    try:
        series = get_series_by_date(videogame_name, date1)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"series_{videogame_name}_{date1:%Y-%m-%d}.json"

    return Response(
        content=json.dumps(series, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
