from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database.database import Base


class Property(Base):
    __tablename__ = "properties"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(100)
    )

    description = Column(
        Text
    )

    price = Column(
        Integer
    )

    location = Column(
        String(100)
    )

    area = Column(
        Integer
    )

    # New field for property filtering
    beds = Column(
        Integer
    )

    # Existing relationship - keep this
    leads = relationship(
        "Lead",
        back_populates="property"
    )