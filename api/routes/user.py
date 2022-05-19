from api.auth.auth_bearer import JWTBearer
from api.auth.auth_handler import decode_jwt
from api.user.user_info import get_user_info
from fastapi import APIRouter, Depends

router = APIRouter()


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


@router.get("/user/{user_id}", tags=['user_profile'])
def get_user(user_id: int):
    return get_user_info(user_id)


@router.get("/user/auth/", tags=['user_profile'])
def get_authenticated_user(current_user_id: int = Depends(get_current_user)):
    return get_user_info(current_user_id)
