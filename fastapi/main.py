from fastapi import FastAPI

# Ligues
from routers.leagues.league_by_period import router as league_period_router
from routers.leagues.league_by_date import router as league_date_router
from routers.leagues.league_by_now import router as league_now_router

# Series
from routers.series.serie_by_period import router as serie_period_router
from routers.series.serie_by_date import router as serie_date_router
from routers.series.serie_by_now import router as serie_now_router

# Tournois
from routers.tournaments.tournament_by_period import router as tournament_period_router
from routers.tournaments.tournament_by_date import router as tournament_date_router
from routers.tournaments.tournament_by_now import router as tournament_now_router

# Matchs
from routers.matches.match_by_period import router as match_period_router
from routers.matches.match_by_date import router as match_date_router
from routers.matches.match_by_now import router as match_now_router
from routers.matches.match_by_time import router as match_time_router
from routers.matches.match_canceled import router as match_canceled_router

app = FastAPI()

app.include_router(league_period_router)
app.include_router(league_date_router)
app.include_router(league_now_router)

app.include_router(serie_period_router)
app.include_router(serie_date_router)
app.include_router(serie_now_router)

app.include_router(tournament_period_router)
app.include_router(tournament_date_router)
app.include_router(tournament_now_router)

app.include_router(match_period_router)
app.include_router(match_date_router)
app.include_router(match_now_router)
app.include_router(match_time_router)
app.include_router(match_canceled_router)

@app.get("/")
async def read_root():
    return {"message": "E-Sport API !!!  Tapez /docs après l'URL pour accéder au Swagger !"} 