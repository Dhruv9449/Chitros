""" Module defining form schemas """

# Imports
import inspect
from typing import Optional, Type
from fastapi import Form
from pydantic import EmailStr, BaseModel

from app.schema.schemas import ORMBase


def form_body(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


# Schemas

@form_body
class UserCreate(ORMBase):
    """ Form schema for creating user """

    fullname: str
    username: str
    email: EmailStr
    password: str


@form_body
class UserUpdate(ORMBase):
    """ Form schema for updating user """

    fullname: Optional[str]
    description: Optional[str]
    email: Optional[EmailStr]


@form_body
class PostCreate(ORMBase):
    """ Form schema for creating post """

    description: Optional[str]
    published: bool
    location: Optional[str]


@form_body
class PostUpdate(PostCreate):
    """ Form schema for updating posts """
    published: Optional[bool]
