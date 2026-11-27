from fastapi import FastAPI
from routers import players, teams

app = FastAPI(title="Football League API")

app.include_router(players.router, prefix="/players", tags=["Players"])
app.include_router(teams.router, prefix="/teams", tags=["Teams"])


@app.get("/")
def root():
    return {"message": "Welcome to the Football League API :D"}
