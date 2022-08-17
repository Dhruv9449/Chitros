""" Module handling the routes for displaying of media items """

# Imports

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db import models
from app.db.db_setup import get_db


# Defining router

router = APIRouter(prefix="/media")


# Getting post images
@router.get("/posts/{image_url}")
async def get_post_image(image_url: str,
                         db: Session = Depends(get_db)) -> any:

    """ Displays post images """

    post = db.query(models.Post).filter(
        models.Post.image_url == f"media/posts/{image_url}").first()

    if post:
        return FileResponse(f"app/media/posts/{image_url}")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No post found")


# Getting user images
@router.get("/users/{image_url}")
async def get_user_image(image_url: str,
                         db: Session = Depends(get_db)) -> any:

    """ Displays user images """

    user = db.query(models.User).filter(
        models.User.profile_pic == f"media/users/{image_url}").first()

    if user:
        return FileResponse(f"app/media/profile_pictures/{image_url}")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="No user found")
