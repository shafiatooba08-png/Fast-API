from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.leads import schemas, service


router = APIRouter(
    prefix="/leads",
    tags=["Leads"]
)


# Database session dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# GET all leads + filter + pagination

@router.get("/", response_model=schemas.LeadListResponse)
def get_leads(
    status: str | None = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return service.get_all_leads(
        db,
        status,
        page,
        limit
    )


# CREATE lead
@router.post(
    "/",
    response_model=schemas.LeadResponse,
    status_code=201
)
def create_lead(
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db)
):
    return service.create_lead(
        db,
        lead
    )


# GET lead by ID

@router.get(
    "/{lead_id}",
    response_model=schemas.LeadDetailResponse
)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    lead = service.get_lead_by_id(
        db,
        lead_id
    )

    if lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return lead

# UPDATE lead (PUT)
@router.put(
    "/{lead_id}",
    response_model=schemas.LeadResponse
)
def update_lead(
    lead_id: int,
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db)
):
    updated_lead = service.update_lead(
        db,
        lead_id,
        lead
    )

    if updated_lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return updated_lead


# PATCH lead
@router.patch(
    "/{lead_id}",
    response_model=schemas.LeadResponse
)
def patch_lead(
    lead_id: int,
    lead: schemas.LeadUpdate,
    db: Session = Depends(get_db)
):
    updated_lead = service.patch_lead(
        db,
        lead_id,
        lead
    )

    if updated_lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return updated_lead


# DELETE lead
@router.delete(
    "/{lead_id}",
    status_code=204
)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db)
):
    deleted_lead = service.delete_lead(
        db,
        lead_id
    )

    if deleted_lead is None:
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    return None