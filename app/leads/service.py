from sqlalchemy.orm import Session, joinedload

from app.leads import models, schemas
from app.core.exceptions import LeadNotFoundError
from app.core.events import emit_event


# GET all leads + status filter + pagination

def get_all_leads(
    db: Session,
    status: str | None = None,
    page: int = 1,
    limit: int = 10,
    user=None
):
    query = db.query(models.Lead)
    # Agent can only see assigned leads
    if user and user.role == "agent":
       query = query.filter(
          models.Lead.agent_id == user.id
        )

    # Existing status filter
    if status is not None:
        query = query.filter(
            models.Lead.status == status
        )

    # Total leads before pagination
    total = query.count()

    # Pagination
    leads = (
        query
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": leads
    }


# CREATE lead

def create_lead(
    db: Session,
    lead: schemas.LeadCreate,
    user
):
    new_lead = models.Lead(
        status=lead.status,
        property_id=lead.property_id,
        customer_id=lead.customer_id,
        agent_id=user.id
    )

    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)

    return new_lead


# GET lead by ID with property and customer

def get_lead_by_id(
    db: Session,
    lead_id: int
):
    lead = (
        db.query(models.Lead)
        .options(
            joinedload(models.Lead.property),
            joinedload(models.Lead.customer)
        )
        .filter(models.Lead.id == lead_id)
        .first()
    )

    if lead is None:
        raise LeadNotFoundError()

    return lead


# UPDATE lead (PUT)

def update_lead(
    db: Session,
    lead_id: int,
    lead: schemas.LeadCreate
):
    existing_lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if existing_lead is None:
        raise LeadNotFoundError()
    old_status = existing_lead.status
    
    existing_lead.status = lead.status
    existing_lead.property_id = lead.property_id
    existing_lead.customer_id = lead.customer_id
   
    db.commit()
    db.refresh(existing_lead)
    if old_status != existing_lead.status:
       emit_event(
           "lead_status_changed",
             existing_lead
        )

    return existing_lead

# PATCH lead

def patch_lead(
    db: Session,
    lead_id: int,
    lead: schemas.LeadUpdate
):
    existing_lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if existing_lead is None:
        raise LeadNotFoundError()
    old_status = existing_lead.status
    if lead.status is not None:
        existing_lead.status = lead.status
  
    if lead.property_id is not None:
        existing_lead.property_id = lead.property_id

    if lead.customer_id is not None:
        existing_lead.customer_id = lead.customer_id

    

    db.commit()
    db.refresh(existing_lead)
    if old_status != existing_lead.status:
       emit_event(
           "lead_status_changed",
            existing_lead
        )

    return existing_lead
# DELETE lead

def delete_lead(
    db: Session,
    lead_id: int
):
    existing_lead = db.query(models.Lead).filter(
        models.Lead.id == lead_id
    ).first()

    if existing_lead is None:
        raise LeadNotFoundError()

    db.delete(existing_lead)
    db.commit()

    return existing_lead