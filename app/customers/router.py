from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.customers import schemas, service

from app.core.permissions import (
    require_agent,
    require_admin
)

from app.users.models import User


router = APIRouter(
    prefix="/customers",
    tags=["Customers"]
)


# Database session dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# GET all customers
# Agent + Admin

@router.get(
    "/",
    response_model=schemas.CustomerListResponse
)
def get_customers(
    status: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    user: User = Depends(require_agent)
):

    return service.get_all_customers(
        db,
        status,
        page,
        limit
    )



# CREATE customer
# Agent + Admin

@router.post(
    "/",
    response_model=schemas.CustomerResponse,
    status_code=201
)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_agent)
):

    created_customer = service.create_customer(
        db,
        customer
    )

    if created_customer is None:
        raise HTTPException(
            status_code=409,
            detail="Customer already exists"
        )

    return created_customer



# GET customer by ID
# Agent + Admin currently
# Customer ownership check will be added later

@router.get(
    "/{customer_id}",
    response_model=schemas.CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_agent)
):

    customer = service.get_customer_by_id(
        db,
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return customer



# UPDATE customer (PUT)
# Agent + Admin

@router.put(
    "/{customer_id}",
    response_model=schemas.CustomerResponse
)
def update_customer(
    customer_id: int,
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_agent)
):

    updated_customer = service.update_customer(
        db,
        customer_id,
        customer
    )

    if updated_customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return updated_customer



# PATCH customer
# Agent + Admin

@router.patch(
    "/{customer_id}",
    response_model=schemas.CustomerResponse
)
def patch_customer(
    customer_id: int,
    customer: schemas.CustomerUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_agent)
):

    updated_customer = service.patch_customer(
        db,
        customer_id,
        customer
    )

    if updated_customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    return updated_customer



# DELETE customer
# Admin only

@router.delete(
    "/{customer_id}"
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin)
):

    deleted_customer = service.delete_customer(
        db,
        customer_id
    )


    if deleted_customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )


    if deleted_customer == "active_leads":
        raise HTTPException(
            status_code=409,
            detail="Customer has active leads and cannot be deleted"
        )


    return {
        "message": "Customer deleted successfully"
    }