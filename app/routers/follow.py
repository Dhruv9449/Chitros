""" Module handling routing and CRUD operations for follow requests and follow feature"""

# Imports

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db import models
from app.db.db_setup import get_db
from app.schema import schemas
from app.auth.oauth2 import get_current_user


# Defining router

router = APIRouter(tags=['Follow Requests'])


# Follow requests and follow feature CRUD

@router.post("/users/{username}/follow", status_code=status.HTTP_201_CREATED)
async def follow(username: str,
                 db: Session = Depends(get_db),
                 current_user: models.User = Depends(get_current_user)) -> any:

    """ Creates a follow request """

    user = db.query(models.User).filter(
        models.User.username == username).first()

    if user == current_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Cannot send yourself a request!")

    if user:
        if user not in current_user.following:
            request = db.query(models.FollowRequest).\
                filter(models.FollowRequest.sender_id == current_user.id,
                       models.FollowRequest.receiver_id == user.id).first()

            if request is None:
                followrequest = models.FollowRequest(
                    sender_id=current_user.id, receiver_id=user.id)
                db.add(followrequest)
                db.commit()
                db.refresh(followrequest)
                return {"Sucess": "request sent!"}

            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Already sent request")

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Already following")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")


@router.delete("/users/{username}/unfollow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow(username: str,
                   db: Session = Depends(get_db),
                   current_user: models.User = Depends(get_current_user)) -> any:

    """ Deletes a following relationship """

    user = db.query(models.User).filter(
        models.User.username == username).first()

    if user:
        if user in current_user.following:
            current_user.unfollow(user)
            db.commit()
            return
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Not following")
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")


@router.get("/requests", response_model=List[schemas.FollowRequest])
async def get_requests(current_user: models.User = Depends(get_current_user)) -> any:

    """ Displays all incomming follow requests"""
    return current_user.received_requests


@router.post("/request/{request_id}/accept", status_code=status.HTTP_201_CREATED)
async def accept_request(request_id: int,
                         db: Session = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)) -> any:

    """ Accepts follow requests and creates a following relationship """

    followrequest_query = db.query(models.FollowRequest).filter(
        models.FollowRequest.id == request_id)
    followrequest = followrequest_query.first()

    if followrequest is not None:
        if followrequest.receiver_id == current_user.id:
            followrequest.sender.follow(current_user)
            followrequest_query.delete(synchronize_session=False)
            db.commit()
            return {"Success": "Requested Accepted"}

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Request does not exist")


@router.delete("/request/{request_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
async def delete_request(request_id: int,
                         db: Session = Depends(get_db),
                         current_user: models.User = Depends(get_current_user)) -> any:

    """ Deletes a follow request and declines a following relationship """

    followrequest_query = db.query(models.FollowRequest).filter(
        models.FollowRequest.id == request_id)
    followrequest = followrequest_query.first()

    if followrequest is not None:
        if followrequest.receiver_id == current_user.id:
            followrequest_query.delete(synchronize_session=False)
            db.commit()
            return

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="Request does not exist")
