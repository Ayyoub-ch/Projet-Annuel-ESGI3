from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from datetime import date

router = APIRouter(prefix="/league", tags=["league"])

# @router.get("/{videogame_name}/")

FOLDER_LEAGUE = "..\..\data_recolt\data\leagues_data"

def get_latest_league(videogame_name: str, league_name: str, id_league: int):
    prefix = f"{FOLDER_LEAGUE}/{videogame_name}/{league_name}/{id_league}.json"