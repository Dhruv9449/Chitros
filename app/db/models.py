""" Module defining all database models"""

# Imports
from sqlalchemy import (TIMESTAMP, Column, ForeignKey,
                        Integer, String, Boolean, Table,
                        select, text, func)
from sqlalchemy.orm import relationship, backref, column_property

from app.db.db_setup import Base


# Table models

user_follow = Table(
    'user_follow', Base.metadata,
    Column('user_id', Integer, ForeignKey(
        "Users.id", ondelete="CASCADE"), primary_key=True),
    Column('following_id', Integer, ForeignKey(
        "Users.id", ondelete="CASCADE"), primary_key=True)
)


class FollowRequest(Base):

    """ Table model for follow requests"""

    __tablename__ = "Follow_Requests"
    id = Column(Integer, primary_key=True, nullable=False)
    sender_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    receiver_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    sender = relationship(
        "User", back_populates="sent_requests", foreign_keys=[sender_id])
    receiver = relationship(
        "User", back_populates="received_requests", foreign_keys=[receiver_id])


class User(Base):

    """ Table model for users """

    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False, unique=True)
    fullname = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    description = Column(String, nullable=True)
    profile_pic = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    following = relationship("User",
                             secondary=user_follow,
                             primaryjoin="User.id==user_follow.c.user_id",
                             secondaryjoin="User.id==user_follow.c.following_id",
                             backref="followers")
    posts = relationship("Post", back_populates="author")
    likes = relationship("Like", back_populates="user")
    comments = relationship("Comment", back_populates="author")
    sent_requests = relationship(
        "FollowRequest", back_populates="sender", foreign_keys=[FollowRequest.sender_id])
    received_requests = relationship(
        "FollowRequest", back_populates="receiver", foreign_keys=[FollowRequest.receiver_id])

    # Methods

    def follow(self, second_user):
        """ Adds user to following """

        if second_user not in self.following:
            self.following.append(second_user)

    def unfollow(self, second_user):
        """ Removes user from following """

        if second_user in self.following:
            self.following.remove(second_user)


class Post(Base):

    """ Table model for posts """

    __tablename__ = "Posts"
    id = Column(Integer, primary_key=True, nullable=False)
    image_url = Column(String, nullable=False)
    description = Column(String, nullable=True)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    location = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    modified_at = Column(TIMESTAMP(timezone=True),
                         nullable=False, server_default=text('now()'))
    author_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")
    comments = relationship("Comment", back_populates="post")


class Comment(Base):

    """ Table model for comments and replies """

    __tablename__ = "Comments"
    id = Column(Integer, primary_key=True, nullable=False)
    author_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="comments")
    content = Column(String, nullable=False)
    post_id = Column(Integer, ForeignKey("Posts.id", ondelete="CASCADE"))
    parent_id = Column(Integer, ForeignKey("Comments.id", ondelete="CASCADE"))
    post = relationship("Post", back_populates="comments")
    replies = relationship(
        "Comment", backref=backref("Comment", remote_side=[id]))
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))


class Like(Base):

    """ Table model for likes """

    __tablename__ = "Likes"
    user_id = Column(Integer, ForeignKey(
        "Users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "Posts.id", ondelete="CASCADE"), primary_key=True)
    post = relationship("Post", back_populates="likes")
    user = relationship("User", back_populates="likes")


# Column Properties
Post.likes_count = column_property(select(func.count(Like.user_id)).
                                   where(Like.post_id == Post.id).
                                   scalar_subquery())
