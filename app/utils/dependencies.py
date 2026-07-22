from fastapi import Depends
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials , HTTPBearer

from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.user import User

from app.utils.jwt import decode_access_token

from app.exceptions.custom_exceptions import (
    AuthenticationException
)

security = HTTPBearer()


def get_current_user(

    credential: HTTPAuthorizationCredentials = Depends(security),

    db: Session = Depends(get_db)

):

    token = credential.credentials
    payload = decode_access_token(token)

    if payload is None:
        raise AuthenticationException(
            "Invalid or expired token"
        )

    email = payload.get("sub")

    if email is None:
        raise AuthenticationException(
            "Invalid token"
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        raise AuthenticationException(
            "User not found"
        )

    return user