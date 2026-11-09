import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.series import get_series_by_period


router = APIRouter(prefix="/serie", tags=["serie"])


@router.get("/{videogame_name}/period")
def download_series_by_period(
    videogame_name: str,
    date1: date,
    date2: date,
):
    """Renvoie toutes les series du jeu comprises dans la période demandée.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    \nDate au format : YYYY-MM-DD"""
    if date1 > date2:
        raise HTTPException(
            status_code=422,
            detail="date1 doit être antérieure ou égale à date2",
        )

    try:
        series = get_series_by_period(videogame_name, date1, date2)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"series_{videogame_name}_{date1:%Y-%m-%d}__to__{date2:%Y-%m-%d}.json"

    return Response(
        content=json.dumps(series, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
