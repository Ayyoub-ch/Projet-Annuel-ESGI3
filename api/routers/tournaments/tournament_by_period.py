import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.tournaments import get_tournaments_by_period


router = APIRouter(prefix="/tournament", tags=["tournament"])


@router.get("/{videogame_name}/period")
def download_tournaments_by_period(
    videogame_name: str,
    date1: date,
    date2: date,
):
    """Renvoie toutes les tournois compris dans la période demandée.
    \nJeu Vidéo : Sans Espace + Avec Majuscule pour chaque Mot
    \nDate au format : YYYY-MM-DD"""
    if date1 > date2:
        raise HTTPException(
            status_code=422,
            detail="date1 doit être antérieure ou égale à date2",
        )

    try:
        tournaments = get_tournaments_by_period(videogame_name, date1, date2)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"tournois_{videogame_name}_{date1:%Y-%m-%d}__to__{date2:%Y-%m-%d}.json"

    return Response(
        content=json.dumps(tournaments, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
