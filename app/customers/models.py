from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100)
    )

    email = Column(
        String(100)
    )

    phone = Column(
        String(20)
    )

    # New field for customer filtering
    status = Column(
        String(20),
        default="active"
    )

    # Existing relationship - keep this
    leads = relationship(
        "Lead",
        back_populates="customer"
    )