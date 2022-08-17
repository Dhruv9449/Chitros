""" Module handling routes for User authentication and creation using login and signup """

# Imports

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import oauth2
from app.auth.utils import get_password, verify_password
from app.schema import schemas, forms
from app.db import models
from app.db.db_setup import get_db


# Defining router

router = APIRouter(tags=['Auth'])


# User signup and login

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: forms.UserCreate = Depends(forms.UserCreate.as_form),
                 db: Session = Depends(get_db)) -> any:

    """ Creates a user """

    if db.query(models.User).filter(models.User.username == user.username).first() is None:
        user.password = get_password(user.password)
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        return {"Success": "User created"}

    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, detail="User exists")


@router.post("/login", response_model=schemas.Token)
async def login(credentials: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(get_db)) -> any:

    """ User login and authentication """

    user = db.query(models.User).filter(
        models.User.username == credentials.username).first()
    if user:
        if verify_password(credentials.password, user.password):
            access_token = oauth2.create_access_token(
                data={"user_id": user.id})

            return {"access_token": access_token, "token_type": "bearer"}

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User doesn't exist")
