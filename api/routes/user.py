import datetime
from typing import Any, List

from api.auth.auth_bearer import JWTBearer
from api.auth.auth_handler import decode_jwt
from api.user.crud.user_action import get_user_info
from fastapi import APIRouter, Depends
from pydantic import BaseModel, EmailStr

router = APIRouter()


class Project(BaseModel):
    project_id: int
    services: List[int]


class UserAction(BaseModel):
    class Source(BaseModel):
        _cls: str
        visit_id: str
        page_id: str

        class Root(BaseModel):
            type: str
        root: Root

    class Target(BaseModel):
        _cls: str
        visit_id: str
        page_id: str

    class Action(BaseModel):
        type: str
        text: str
        order: bool

    unique_id: str
    timestamp: datetime.datetime
    source: Source
    target: Target
    action: Action


class Recommendation(BaseModel):
    timestamp: datetime.datetime
    page_id: str
    panel_id: str
    services: List[int]


class User(BaseModel):
    user_id: int
    scientific_domains: List[str]
    categories: List[str]
    projects: List[Project]
    user_actions: List[UserAction]
    recommendations: List[Recommendation]


async def get_current_user(token: str = Depends(JWTBearer())):
    """
    This method makes the assumption that the payload of JWT is
    {
        expires: xxx
        user_id: 586
    }
    """
    payload = decode_jwt(token)

    return payload['user_id']


@router.get("/user/{user_id}", tags=['user_profile'], response_model=User)
def get_user(user_id: int):
    return get_user_info(user_id)


@router.get("/user/auth/", tags=['user_profile'], response_model=User)
def get_authenticated_user(current_user_id: int = Depends(get_current_user)):
    return get_user_info(current_user_id)
