from sqlalchemy.orm import Session

from app.models.user import User

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.utils.hashing import (
    hash_password,
    verify_password
)

from app.utils.jwt import create_access_token

from app.exceptions.custom_exceptions import (
    DuplicateRecordException,
    AuthenticationException
)


class AuthService:

    @staticmethod
    def register(
        db: Session,
        request: RegisterRequest
    ):

        existing_user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if existing_user:
            raise DuplicateRecordException(
                "Email already registered"
            )

        user = User(
            full_name=request.full_name,
            email=request.email,
            password=hash_password(request.password),
            role=request.role
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def login(
        db: Session,
        request: LoginRequest
    ) -> TokenResponse:

        user = (
            db.query(User)
            .filter(User.email == request.email)
            .first()
        )

        if user is None:
            raise AuthenticationException(
                "Invalid email or password"
            )

        if not verify_password(
            request.password,
            user.password
        ):
            raise AuthenticationException(
                "Invalid email or password"
            )

        token = create_access_token(
            {
                "sub": user.email,
                "role": user.role.value
            }
        )

        return TokenResponse(
            access_token=token
        )