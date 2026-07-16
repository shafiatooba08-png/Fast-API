from sqlalchemy.orm import Session

from app.customers import models, schemas


# GET all customers + filters + pagination

def get_all_customers(
    db: Session,
    status: str | None = None,
    page: int = 1,
    limit: int = 10
):
    query = db.query(models.Customer)

    # Existing status filter
    if status is not None:
        query = query.filter(
            models.Customer.status == status
        )

    # Total customers before pagination
    total = query.count()

    # Pagination
    customers = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": customers
    }


# CREATE customer

def create_customer(
    db: Session,
    customer: schemas.CustomerCreate
):
    new_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        status=customer.status
    )

    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)

    return new_customer


# GET customer by ID

def get_customer_by_id(
    db: Session,
    customer_id: int
):
    return db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()


# UPDATE customer (PUT)

def update_customer(
    db: Session,
    customer_id: int,
    customer: schemas.CustomerCreate
):
    existing_customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if existing_customer is None:
        return None

    existing_customer.name = customer.name
    existing_customer.email = customer.email
    existing_customer.phone = customer.phone
    existing_customer.status = customer.status

    db.commit()
    db.refresh(existing_customer)

    return existing_customer


# PATCH customer

def patch_customer(
    db: Session,
    customer_id: int,
    customer: schemas.CustomerUpdate
):
    existing_customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if existing_customer is None:
        return None

    if customer.name is not None:
        existing_customer.name = customer.name

    if customer.email is not None:
        existing_customer.email = customer.email

    if customer.phone is not None:
        existing_customer.phone = customer.phone

    if customer.status is not None:
        existing_customer.status = customer.status

    db.commit()
    db.refresh(existing_customer)

    return existing_customer


def delete_customer(
    db: Session,
    customer_id: int
):
    existing_customer = db.query(models.Customer).filter(
        models.Customer.id == customer_id
    ).first()

    if existing_customer is None:
        return None

    # Check active leads before deleting
    if existing_customer.leads:
        return "active_leads"

    db.delete(existing_customer)
    db.commit()

    return existing_customer