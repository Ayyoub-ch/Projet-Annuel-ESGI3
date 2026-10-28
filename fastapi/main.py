from fastapi import FastAPI

from routers.leagues.league_by_period import router as league_period_router
from routers.leagues.league_by_date import router as league_date_router

app = FastAPI()
app.include_router(league_period_router)
app.include_router(league_date_router)

@app.get("/")
async def read_root():
    return {"message": "Salam !"} 