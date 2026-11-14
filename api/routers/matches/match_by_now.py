import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.matches import get_matches_by_now


router = APIRouter(prefix="/match", tags=["match"])


@router.get("/{videogame_name}/now")
def download_matches_by_now(
    videogame_name: str
    ):
    """Renvoie toutes les matchs compris entre la date d'aujourd'hui et les dates inférieures ou égal à elle-même.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    """
    date_now = date.today()

    try:
        matches = get_matches_by_now(videogame_name)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"matchs_{videogame_name}_{date_now:%Y-%m-%d}.json"

    return Response(
        content=json.dumps(matches, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
