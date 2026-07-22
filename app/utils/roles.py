from fastapi import Depends

from app.models.user import UserRole

from app.utils.dependencies import get_current_user

from app.exceptions.custom_exceptions import (
    AuthorizationException
)


def require_admin(current_user=Depends(get_current_user)):

    if current_user.role != UserRole.ADMIN:
        raise AuthorizationException(
            "Admin access required"
        )

    return current_user


def require_owner(current_user=Depends(get_current_user)):

    if current_user.role not in [
        UserRole.ADMIN,
        UserRole.OWNER
    ]:
        raise AuthorizationException(
            "Owner access required"
        )

    return current_user


def require_tenant(current_user=Depends(get_current_user)):

    if current_user.role != UserRole.TENANT:
        raise AuthorizationException(
            "Tenant access required"
        )

    return current_user


def require_admin_or_owner(
    current_user=Depends(get_current_user)
):

    if current_user.role not in [
        UserRole.ADMIN,
        UserRole.OWNER
    ]:

        raise AuthorizationException(
            "Admin or Owner access required"
        )

    return current_user