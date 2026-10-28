import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.leagues import get_leagues_by_now


router = APIRouter(prefix="/league", tags=["league"])


@router.get("/{videogame_name}/now")
def download_leagues_by_now(
    videogame_name: str
    ):
    """Renvoie toutes les ligues du jeu comprises à la date d'aujourd"hui.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    """
    date_now = date.today()

    try:
        leagues = get_leagues_by_now(videogame_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"ligues_{videogame_name}_{date_now:%Y-%m-%d}.json"

    return Response(
        content=json.dumps(leagues, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
