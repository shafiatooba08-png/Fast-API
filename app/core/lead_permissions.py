from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.leads import service
from app.core.security import get_current_user
from app.core.exceptions import PermissionDeniedError
from app.users.models import User


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def require_lead_access(
    lead_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):

    lead = service.get_lead_by_id(
        db,
        lead_id
    )

    if lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )


    if user.role == "admin":
        return lead


    if user.role == "agent":

        if lead.agent_id != user.id:
            raise PermissionDeniedError()

        return lead


    raise PermissionDeniedError()