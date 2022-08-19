""" Module handling routes and CRUD operations for Posts """

# imports

from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile
from sqlalchemy import desc
from sqlalchemy.orm import Session
from PIL import Image

from app.auth.oauth2 import get_current_user
from app.schema import schemas, forms
from app.db import models
from app.db.db_setup import get_db

# Router

router = APIRouter(tags=['Posts'])


# Feed router
@router.get("/feed", response_model=List[schemas.PostResponse])
async def get_posts(page: Optional[int] = 1, sort: Optional[str] = None,
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)) -> any:

    """ Displays users feed"""

    post_query = db.query(models.Post).\
        join(models.User).\
        filter(models.Post.author_id.in_([user.id for user in
                                          current_user.following +
                                          [current_user]]),
               models.Post.published == True)

    if sort == "likes":
        post_query = post_query.order_by(
            desc(models.Post.likes_count))
    else:
        post_query = post_query.order_by(models.Post.created_at.desc())

    start = 10*(page-1)
    stop = start+10
    posts = post_query.slice(start, stop).all()

    return posts


# Posts CRUD

@router.post("/createpost", status_code=status.HTTP_201_CREATED)
async def create_post(post: forms.PostCreate = Depends(forms.PostCreate.as_form),
                      image: UploadFile = File(...),
                      db: Session = Depends(get_db),
                      current_user: int = Depends(get_current_user)) -> any:

    """ Create a post """

    file_extension = "." + image.filename.split(".")[-1]

    if file_extension in [".png", ".jpg", ".jpeg"]:

        post_datetime = datetime.utcnow().strftime("%Y%d%m%H%M%S")
        filename = str(current_user.id) + "_" + post_datetime + file_extension
        path = f"app/media/posts/{filename}"
        newpost = models.Post(author_id=current_user.id,
                              **post.dict(), image_url=f"media/posts/{filename}")
        with open(path, "wb") as file:
            file.write(await image.read())

        image = Image.open(path)
        image.thumbnail((732, 732))
        image.save(path)

        db.add(newpost)
        db.commit()

        return {"Success": "Added post!"}

    raise HTTPException(
        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


@router.get("/{username}/{post_id}", response_model=schemas.PostResponse)
async def get_post(username: str,
                   post_id: int,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)) -> any:

    """ View user's post """

    user = db.query(models.User).filter(
        models.User.username == username).first()

    if user not in current_user.following and user is not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not in following")

    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if post:
        return post

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exist")


@router.put("/{username}/{post_id}",
            status_code=status.HTTP_202_ACCEPTED)
async def edit_post(username: str,
                    post_id: int,
                    new_data: forms.PostUpdate = Depends(
                        forms.PostUpdate.as_form),
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)) -> any:

    """ Edit user's post """

    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not allowed")

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post:
        post_query.modified_at: datetime = datetime.now()
        new_data_dict = {field: value for field, value in new_data.dict().items()
                         if value is not None}
        post_query.update(new_data_dict, synchronize_session=False)
        db.commit()

        return {"Success": "post updated"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exist")


@router.delete("/{username}/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(username: str,
                      post_id: int,
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)) -> any:

    """ Delete user's post"""

    if current_user.username != username:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if post:
        post_query.delete(synchronize_session=False)
        db.commit()
        return

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Post doesn't exist")
