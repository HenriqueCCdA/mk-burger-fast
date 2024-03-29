from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import router_burger, router_ingredients_status

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_burger)
app.include_router(router_ingredients_status)
