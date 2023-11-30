from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes.categories import router as categories_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories_router, prefix="/categories", tags=["Categories"])
