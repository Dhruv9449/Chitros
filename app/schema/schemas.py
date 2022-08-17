""" Module defining response and other schemas """

# Imports

from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# Schemas

class ORMBase(BaseModel):
    """ Base for ORM models"""

    class Config:
        """ Configuring ORM mode to true"""
        orm_mode = True


class UserFollow(ORMBase):
    """ Schema for displaying users in short way """
    id: int
    fullname: str
    username: str
    profile_pic: Optional[str]


class UserProfileViewUnfollower(ORMBase):
    """ Schema for displaying users if they are not followed by the user """
    id: int
    fullname: str
    username: str
    profile_pic: Optional[str]
    description: Optional[str]
    follower_count: int
    following_count: int


class ReplyResponse(ORMBase):
    """ Reply response schema """
    author_id: int
    parent_id: int
    author: UserFollow
    content: str


class CommentResponse(ORMBase):
    """ Comment response schema """
    id: int
    post_id: int
    author_id: int
    author: UserFollow
    content: str
    replies: List[ReplyResponse]


class LikeResponse(ORMBase):
    """ Like response schema """
    user_id: int
    post_id: int
    user: UserFollow


class PostResponse(ORMBase):
    """ Post response schema """
    id: int
    author: UserFollow
    image_url: str
    description: Optional[str]
    location: Optional[str]
    created_at: datetime
    likes: List[LikeResponse]
    comments: List[CommentResponse]


class UserProfileView(ORMBase):
    """ User profile response schema """
    id: int
    username: str
    fullname: str
    profile_pic: Optional[str]
    description: Optional[str]
    posts: List[PostResponse]
    following: List[UserFollow]
    followers: List[UserFollow]


class FollowRequestCreate(ORMBase):
    """ Follow request create schema """
    author_id: int
    receiver_id: int


class FollowRequest(ORMBase):
    """ Follow request response schema """
    id: int
    sender_id: int
    receiver_id: int
    sender: UserFollow


class CommentCreate(ORMBase):
    """ Comment create schema """
    content: str


class Token(BaseModel):
    """ JWT Token schema """
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """ Token data schema """
    id: Optional[int]
