from fastapi import FastAPI
import time
import os


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

start = time.time()

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
    return {"message": "API E-Sport - SportSphere opérationnel"} 

app.on_event("startup")
async def startup_event():
    logger.info("Starting E-Sport API...")
    logger.info(f"Startup time: {time.time() - start} seconds")
    
app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down E-Sport API...")
    
    
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)