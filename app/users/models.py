from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class User(Base):

    __tablename__ = "users"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    username = Column(
        String,
        unique=True,
        nullable=False
    )


    hashed_password = Column(
        String,
        nullable=False
    )


    role = Column(
        String,
        nullable=False
    )


    # One user can have one customer profile
    # Used for customer role access control

    customer = relationship(
        "Customer",
        back_populates="user",
        uselist=False
    )