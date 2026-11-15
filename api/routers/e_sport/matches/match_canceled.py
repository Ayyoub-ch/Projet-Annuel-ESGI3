import json
from datetime import date

from fastapi import APIRouter, HTTPException, Response

from services.e_sport.matches import get_matches_canceled


router = APIRouter(prefix="/e-sport/match", tags=["e-sport"])


@router.get("/cancel")
def download__matches_canceled(
    ):
    """Renvoie toutes les matchs annulés"""
    try:
        matches = get_matches_canceled()
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Jeu introuvable")

    # Remplace les caractères qui ne conviennent pas à un nom de fichier.
    filename = f"matchs_canceled.json"

    return Response(
        content=json.dumps(matches, ensure_ascii=False, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
