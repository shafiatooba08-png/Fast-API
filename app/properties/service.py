from sqlalchemy.orm import Session
from app.properties import models


# GET all properties + filters

def get_all_properties(
    db: Session,
    beds: int | None = None,
    location: str | None = None,
    min_price: int | None = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(models.Property)

    # Existing filters
    if beds is not None:
        query = query.filter(
            models.Property.beds == beds
        )

    if location is not None:
        query = query.filter(
            models.Property.location == location
        )

    if min_price is not None:
        query = query.filter(
            models.Property.price >= min_price
        )

    # Total records before pagination
    total = query.count()

    # Pagination
    properties = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": properties
    }


# CREATE property

def create_property(db: Session, property_data):
    new_property = models.Property(
        title=property_data.title,
        description=property_data.description,
        price=property_data.price,
        location=property_data.location,
        area=property_data.area,
        beds=property_data.beds
    )

    db.add(new_property)
    db.commit()
    db.refresh(new_property)

    return new_property


# GET property by ID

def get_property_by_id(db: Session, property_id: int):
    return db.query(models.Property).filter(
        models.Property.id == property_id
    ).first()


# UPDATE property

def update_property(db: Session, property_id: int, property_data):

    existing_property = db.query(models.Property).filter(
        models.Property.id == property_id
    ).first()

    if existing_property is None:
        return None

    existing_property.title = property_data.title
    existing_property.description = property_data.description
    existing_property.price = property_data.price
    existing_property.location = property_data.location
    existing_property.area = property_data.area
    existing_property.beds = property_data.beds

    db.commit()
    db.refresh(existing_property)

    return existing_property


# DELETE property

def delete_property(db: Session, property_id: int):

    property = db.query(models.Property).filter(
        models.Property.id == property_id
    ).first()

    if property is None:
        return None

    db.delete(property)
    db.commit()

    return property


# PATCH property

def patch_property(db: Session, property_id: int, property_data):

    existing_property = db.query(models.Property).filter(
        models.Property.id == property_id
    ).first()

    if existing_property is None:
        return None

    if property_data.title is not None:
        existing_property.title = property_data.title

    if property_data.description is not None:
        existing_property.description = property_data.description

    if property_data.price is not None:
        existing_property.price = property_data.price

    if property_data.location is not None:
        existing_property.location = property_data.location

    if property_data.area is not None:
        existing_property.area = property_data.area

    if property_data.beds is not None:
        existing_property.beds = property_data.beds

    db.commit()
    db.refresh(existing_property)

    return existing_property