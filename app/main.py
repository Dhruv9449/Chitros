"""
 ██████╗██╗  ██╗██╗████████╗██████╗  ██████╗ ███████╗
██╔════╝██║  ██║██║╚══██╔══╝██╔══██╗██╔═══██╗██╔════╝
██║     ███████║██║   ██║   ██████╔╝██║   ██║███████╗
██║     ██╔══██║██║   ██║   ██╔══██╗██║   ██║╚════██║
╚██████╗██║  ██║██║   ██║   ██║  ██║╚██████╔╝███████║
 ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝

Chitros is a social media backend API made using FastAPI

Version - 0.0.1
License - MIT

Developed with 💙️ by Dhruv Shah
"""

# Imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import app_settings
from app.db import models
from app.db.db_setup import engine
from app.routers import post, user, follow, like, comment, auth, media


# Creating all database models
models.Base.metadata.create_all(bind=engine)


# Creating FastAPI app
app = FastAPI(**app_settings.dict())


# Allowed origins for CORS
origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://127.0.0.1:5500"

]


# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root
@app.get('/')
async def root():
    """ Root function """
    return {"message": "Welcome to Chitros API"}


# Registering all routers to the app

app.include_router(follow.router)
app.include_router(like.router)
app.include_router(comment.router)
app.include_router(media.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
