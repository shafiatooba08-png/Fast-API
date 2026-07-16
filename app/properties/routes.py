from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.properties import schemas, service


router = APIRouter(
    prefix="/properties",
    tags=["Properties"]
)


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET all properties + filters

@router.get("/", response_model=schemas.PropertyListResponse)
def get_properties(
    beds: int | None = None,
    location: str | None = None,
    min_price: int | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return service.get_all_properties(
        db,
        beds,
        location,
        min_price,
        page,
        limit
    )


# CREATE property
@router.post(
    "/",
    response_model=schemas.PropertyResponse,
    status_code=201
)
def create_property(
    property: schemas.PropertyCreate,
    db: Session = Depends(get_db)
):
    return service.create_property(db, property)


# GET property by ID
@router.get("/{property_id}", response_model=schemas.PropertyResponse)
def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    property = service.get_property_by_id(db, property_id)

    if property is None:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return property


# UPDATE property (PUT)
@router.put("/{property_id}", response_model=schemas.PropertyResponse)
def update_property(
    property_id: int,
    property: schemas.PropertyCreate,
    db: Session = Depends(get_db)
):
    updated_property = service.update_property(
        db,
        property_id,
        property
    )

    if updated_property is None:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return updated_property


# DELETE property
@router.delete(
    "/{property_id}",
    status_code=204
)
def delete_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    deleted_property = service.delete_property(
        db,
        property_id
    )

    if deleted_property is None:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return None


# PATCH property (partial update)
@router.patch(
    "/{property_id}",
    response_model=schemas.PropertyResponse
)
def patch_property(
    property_id: int,
    property: schemas.PropertyUpdate,
    db: Session = Depends(get_db)
):
    updated_property = service.patch_property(
        db,
        property_id,
        property
    )

    if updated_property is None:
        raise HTTPException(
            status_code=404,
            detail="Property not found"
        )

    return updated_property