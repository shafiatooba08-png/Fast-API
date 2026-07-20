from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class Customer(Base):

    __tablename__ = "customers"


    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # Link customer profile with user account
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        unique=True
    )


    name = Column(
        String(100),
        nullable=False
    )


    email = Column(
        String(100),
        nullable=False,
        unique=True,
        index=True
    )


    phone = Column(
        String(20),
        nullable=False
    )


    status = Column(
        String(20),
        nullable=False,
        default="active",
        index=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


    # User relationship
    user = relationship(
        "User",
        back_populates="customer",
        uselist=False
    )


    # Existing relationship - keep this

    leads = relationship(
        "Lead",
        back_populates="customer"
    )