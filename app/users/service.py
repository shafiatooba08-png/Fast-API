from sqlalchemy.orm import Session

from app.users import models, schemas
from passlib.context import CryptContext
from app.core.exceptions import UsernameAlreadyExistsError


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


# Hash password
def hash_password(password):
    return pwd_context.hash(password)


# Verify password
def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


# Authenticate user
def authenticate_user(
    db: Session,
    username: str,
    password: str
):

    user = (
        db.query(models.User)
        .filter(
            models.User.username == username
        )
        .first()
    )

    if user is None:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user


# Keep your existing create_user function below
def create_user(
    db: Session,
    user: schemas.UserCreate
):

    existing_user = (
        db.query(models.User)
        .filter(
            models.User.username == user.username
        )
        .first()
    )

    if existing_user:
        raise UsernameAlreadyExistsError()

    hashed_password = hash_password(
        user.password
    )

    new_user = models.User(
        username=user.username,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user