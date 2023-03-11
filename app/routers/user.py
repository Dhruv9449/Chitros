""" Module handling routes and CRUD operations for Users """

# Imports

from typing import List, Optional, Union
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy import or_
from sqlalchemy.orm import Session
from PIL import Image

from app.schema import schemas, forms
from app.db import models
from app.db.db_setup import get_db
from app.auth.oauth2 import get_current_user

# Defining router

router = APIRouter(prefix="/users",
                   tags=['Users']
                   )


# User search
@router.get("/", response_model=List[schemas.UserFollow])
async def search_users(search: str = " ",
                       db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)) -> any:

    """ Searches for users with similar username/name as the query """
    
    if search == " ":
      users = db.query(models.User).all()
      return users

    search_query = f"%{search}%"
    users = db.query(models.User).filter(or_(models.User.username.ilike(search_query),
                                             models.User.fullname.ilike(
                                                 search_query),
                                             models.User.description.ilike(search_query))).all()

    return users


# Users CRUD

@router.get("/{username}", response_model=Union[schemas.UserProfileView,
                                                schemas.UserProfileViewUnfollower])
async def get_user(username: str, db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)) -> any:

    """ Displays a user """

    user = db.query(models.User).filter(
        models.User.username == username).first()

    if user:
        if user == current_user:
            return schemas.UserProfileView.from_orm(user)
        if user in current_user.following:
            user_response = schemas.UserProfileView.from_orm(user)
            user_response.posts = db.query(models.Post).filter(
                models.Post.author == user, models.Post.published == True).all()
            return user_response

        user.follower_count = len(user.followers)
        user.following_count = len(user.following)
        user_response = schemas.UserProfileViewUnfollower.from_orm(user)

        return user_response

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")


@router.put("/{username}")
async def edit_user(username: str,
                    profile_pic: Optional[UploadFile] = None,
                    new_data: forms.UserUpdate = Depends(
                        forms.UserUpdate.as_form),
                    db: Session = Depends(get_db),
                    current_user: models.User = Depends(get_current_user)) -> any:

    """ Updates a user """

    if username == current_user.username:
        if profile_pic:
            file_extension = "." + profile_pic.filename.split(".")[-1]
            if file_extension in [".png", ".jpg", ".jpeg"]:
                filename = f"{current_user.id}_{current_user.username}{file_extension}"
                path = f"app/media/profile_pictures/{filename}"
                with open(path, "wb") as file:
                    file.write(await profile_pic.read())

                profile_pic = f"media/users/{filename}"
                image = Image.open(path)
                image.resize((400, 400)).save(path)

            else:
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        new_data_dict = {field: value for field,
                         value in {**new_data.dict(),
                                   **{"profile_pic": profile_pic}}.items()
                         if value is not None}

        db.query(models.User).filter(models.User.id == current_user.id).\
            update(new_data_dict,
                   synchronize_session=False)

        db.commit()
        return {"Success": "User updated"}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Cannot edit other's profiles")


@ router.delete("/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(username: str,
                      db: Session = Depends(get_db),
                      current_user: models.User = Depends(get_current_user)) -> any:

    """ Deletes a user """

    if username == current_user.username:

        db.query(models.User).filter(models.User.username ==
                                     username).delete(synchronize_session=False)
        db.commit()
        return

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Cannot delete other's profiles")
