""" Module handling routes CRUD operations for Comments and Replies """

# Imports

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schema import schemas
from app.db import models
from app.db.db_setup import get_db
from app.auth.oauth2 import get_current_user

# Defining router

router = APIRouter(tags=["Comments"])


# Comments CRUD

@router.post("/{post_id}/comment", status_code=status.HTTP_201_CREATED)
async def post_comment(post_id: int,
                       content: schemas.CommentCreate,
                       db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)) -> any:

    """ Creates a comment """

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post:
        if post.author in current_user.following or post.author == current_user:
            comment = models.Comment(post=post,
                                     author=current_user,
                                     **content.dict())
            db.add(comment)
            db.commit()
            return {"Success": "Comment added!"}

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not following")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.delete("/{post_id}/{comment_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(comment_id: int,
                         db: Session = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)) -> any:

    """ Deletes a comment """

    comment_query = db.query(models.Comment).filter(
        models.Comment.id == comment_id)
    comment = comment_query.first()

    if comment:
        if comment.author == current_user:
            comment_query.delete(synchronize_session=False)
            db.commit()
            return

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Cannot delete other users comments")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


# Replies CRUD


@router.post("/{post_id}/{comment_id}/reply", status_code=status.HTTP_201_CREATED)
async def post_reply(post_id: int,
                     comment_id: int,
                     content: schemas.CommentCreate,
                     db: Session = Depends(get_db),
                     current_user: models.User = Depends(get_current_user)) -> any:

    """ Creates a reply  """

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post:
        comment = db.query(models.Comment).filter(
            models.Comment.id == comment_id, models.Comment.post_id == post.id, models.Comment.parent_id == None).first()

        if comment:
            if post.author in current_user.following or post.author == current_user:
                reply = models.Comment(parent_id=comment_id,
                                       author=current_user,
                                       **content.dict())
                db.add(reply)
                db.commit()
                return {"Success": "Reply added!"}

            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Not following")

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.delete("/{post_id}/{comment_id}/{reply_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reply(reply_id: int,
                       db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)) -> any:

    """ Deletes a reply """

    reply_query = db.query(models.Comment).filter(
        models.Comment.id == reply_id)
    reply = reply_query.first()

    if reply:
        if reply.author == current_user:

            reply_query.delete(synchronize_session=False)
            db.commit()
            return

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Cannot delete other users comments")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
