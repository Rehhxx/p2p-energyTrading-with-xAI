from fastapi import FastAPI
from .routes import trade_routes

app = FastAPI()

app.include_router(trade_routes.router, prefix = "/api")

@app.get("/")
def root():
    return {"message": "P2P Energy Trading API Running"}
