import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.series import get_series_by_now


router = APIRouter(prefix="/serie", tags=["serie"])


@router.get("/{videogame_name}/now")
def download_series_by_now(
    videogame_name: str
    ):
    """Renvoie toutes les series du jeu comprises à la date d'aujourd"hui.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    """
    date_now = date.today()

    try:
        series = get_series_by_now(videogame_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"series_{videogame_name}_{date_now:%Y-%m-%d}.json"

    return Response(
        content=json.dumps(series, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
