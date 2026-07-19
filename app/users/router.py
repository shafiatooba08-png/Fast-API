from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.users import service, schemas
from app.database.database import get_db
from app.core.jwt import create_access_token


router = APIRouter(
    prefix="/users",
    tags=["users"]
)


# Create User
@router.post("/", response_model=schemas.UserResponse, status_code=201)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db)
):
    return service.create_user(db, user)


# Login User (JSON body)
@router.post("/login", response_model=schemas.TokenResponse)
def login(
    user: schemas.LoginRequest,
    db: Session = Depends(get_db)
):

    db_user = service.authenticate_user(
        db,
        user.username,
        user.password
    )

    if db_user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    token = create_access_token(
        {
            "sub": str(db_user.id),
            "role": db_user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }