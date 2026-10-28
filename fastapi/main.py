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
from routers.series.serie_by_period import router as serie_period_router
from routers.series.serie_by_date import router as serie_date_router
from routers.series.serie_by_now import router as serie_now_router


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

@app.get("/")
async def read_root():
    return {"message": "E-Sport API !!!  Tapez /docs après l'URL pour accéder au Swagger !"} 