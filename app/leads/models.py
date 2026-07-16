from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    status = Column(
        String,
        default="new"
    )

    property_id = Column(
        Integer,
        ForeignKey("properties.id")
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id")
    )


    property = relationship(
        "Property",
        back_populates="leads"
    )

    customer = relationship(
        "Customer",
        back_populates="leads"
    )