from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.routers import api

app = FastAPI()

app.include_router(api.router)

app.mount("/", StaticFiles(directory="src/static"), name="static")
