from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.customers import schemas, service


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
@router.get("/", response_model=schemas.CustomerListResponse)
def get_customers(
    status: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return service.get_all_customers(
        db,
        status,
        page,
        limit
    )


# CREATE customer
@router.post(
    "/",
    response_model=schemas.CustomerResponse,
    status_code=201
)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    return service.create_customer(
        db,
        customer
    )


# GET customer by ID
@router.get(
    "/{customer_id}",
    response_model=schemas.CustomerResponse
)
def get_customer(
    customer_id: int,
    db: Session = Depends(get_db)
):
    return service.get_customer_by_id(
        db,
        customer_id
    )
# UPDATE customer (PUT)
@router.put(
    "/{customer_id}",
    response_model=schemas.CustomerResponse
)
def update_customer(
    customer_id: int,
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
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
@router.patch(
    "/{customer_id}",
    response_model=schemas.CustomerResponse
)
def patch_customer(
    customer_id: int,
    customer: schemas.CustomerUpdate,
    db: Session = Depends(get_db)
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


@router.delete(
    "/{customer_id}"
)
def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db)
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