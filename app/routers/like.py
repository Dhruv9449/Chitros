""" Module handling routes and CRUD operations for Likes """

# Imports

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.db.db_setup import get_db
from app.auth.oauth2 import get_current_user


# Defining router

router = APIRouter(tags=["Likes"])


# Comments CRUD

@router.post("/{post_id}/like", status_code=status.HTTP_201_CREATED)
async def like_post(post_id: int,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)) -> any:

    """ Creates a like on the post"""

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post:
        if post.author in current_user.following:
            if current_user not in [like.user for like in post.likes]:
                like = models.Like(post=post, user=current_user)
                db.add(like)
                db.commit()
                return {"Success": "Liked post!"}

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already liked post")

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not following")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.delete("/{post_id}/unlike", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_post(post_id: int, db: Session = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)) -> any:

    """ Deletes a like from the post """

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post:
        if post.author in current_user.following:
            if current_user in [like.user for like in post.likes]:
                db.query(models.Like).filter(models.Like.user_id ==
                                             current_user.id).delete(synchronize_session=False)
                db.commit()
                return

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already unliked")

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not following")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
