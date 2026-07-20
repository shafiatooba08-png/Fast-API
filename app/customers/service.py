from sqlalchemy.orm import Session

from app.customers import models, schemas


# GET all customers + filters + pagination

def get_all_customers(
    db: Session,
    status: str | None = None,
    page: int = 1,
    limit: int = 10
):

    # prevent invalid pagination
    if page < 1:
        page = 1

    if limit < 1 or limit > 100:
        limit = 10


    query = db.query(models.Customer)


    # status filter
    if status is not None:
        query = query.filter(
            models.Customer.status == status
        )


    # total records before pagination
    total = query.count()


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

    # duplicate email check
    existing_customer = db.query(
        models.Customer
    ).filter(
        models.Customer.email == customer.email
    ).first()


    if existing_customer:
        return None


    new_customer = models.Customer(
        name=customer.name,
        email=customer.email,
        phone=customer.phone,
        status=customer.status
    )


    try:

        db.add(new_customer)
        db.commit()
        db.refresh(new_customer)

    except Exception:

        db.rollback()
        raise


    return new_customer



# GET customer by ID

def get_customer_by_id(
    db: Session,
    customer_id: int
):

    return db.query(
        models.Customer
    ).filter(
        models.Customer.id == customer_id
    ).first()



# UPDATE customer

def update_customer(
    db: Session,
    customer_id: int,
    customer: schemas.CustomerUpdate
):

    existing_customer = db.query(
        models.Customer
    ).filter(
        models.Customer.id == customer_id
    ).first()


    if existing_customer is None:
        return None



    # check duplicate email only when email is being updated
    if customer.email is not None:

        email_exists = db.query(
            models.Customer
        ).filter(
            models.Customer.email == customer.email,
            models.Customer.id != customer_id
        ).first()


        if email_exists:
            return None



    if customer.name is not None:
        existing_customer.name = customer.name


    if customer.email is not None:
        existing_customer.email = customer.email


    if customer.phone is not None:
        existing_customer.phone = customer.phone


    if customer.status is not None:
        existing_customer.status = customer.status



    try:

        db.commit()
        db.refresh(existing_customer)

    except Exception:

        db.rollback()
        raise


    return existing_customer



# PATCH customer

def patch_customer(
    db: Session,
    customer_id: int,
    customer: schemas.CustomerUpdate
):

    existing_customer = db.query(
        models.Customer
    ).filter(
        models.Customer.id == customer_id
    ).first()


    if existing_customer is None:
        return None



    # email duplicate check during patch
    if customer.email is not None:

        email_exists = db.query(
            models.Customer
        ).filter(
            models.Customer.email == customer.email,
            models.Customer.id != customer_id
        ).first()


        if email_exists:
            return None



    if customer.name is not None:
        existing_customer.name = customer.name


    if customer.email is not None:
        existing_customer.email = customer.email


    if customer.phone is not None:
        existing_customer.phone = customer.phone


    if customer.status is not None:
        existing_customer.status = customer.status



    try:

        db.commit()
        db.refresh(existing_customer)

    except Exception:

        db.rollback()
        raise


    return existing_customer



# DELETE customer

def delete_customer(
    db: Session,
    customer_id: int
):

    existing_customer = db.query(
        models.Customer
    ).filter(
        models.Customer.id == customer_id
    ).first()



    if existing_customer is None:
        return None



    # business rule:
    # customer with leads cannot be deleted

    if existing_customer.leads:
        return "active_leads"



    try:

        db.delete(existing_customer)
        db.commit()

    except Exception:

        db.rollback()
        raise



    return existing_customer