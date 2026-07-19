from fastapi import Depends

from app.core.security import  get_current_user
from app.core.exceptions import PermissionDeniedError
from app.users.models import User


def require_admin(
    user: User = Depends(get_current_user)
):
    if user.role != "admin":
        raise PermissionDeniedError()

    return user


def require_agent(
    user: User = Depends(get_current_user)
):
    if user.role not in ["agent", "admin"]:
        raise PermissionDeniedError()

    return user

def require_customer(
    user: User = Depends(get_current_user)
):
    if user.role not in ["customer", "admin"]:
        raise PermissionDeniedError()

    return user