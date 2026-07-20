from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import SessionLocal
from app.leads import schemas, service
from app.core.permissions import require_agent, require_admin
from app.core.lead_permissions import require_lead_access
from app.core.rate_limit import rate_limiter
from app.users.models import User

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
    db: Session = Depends(get_db),
    user: User = Depends(require_agent)
):
    return service.get_all_leads(
        db,
        status,
        page,
        limit,
        user
    )


# CREATE lead

@router.post(
    "/",
    response_model=schemas.LeadResponse,
    status_code=201
)
def create_lead(
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_agent),
    _ = Depends(rate_limiter)
):
    print(">>> create_lead endpoint reached <<<")

    return service.create_lead(
        db,
        lead,
        user
    )


# GET lead by ID

@router.get(
    "/{lead_id}",
    response_model=schemas.LeadDetailResponse
)
def get_lead(
    lead_id: int,
    lead = Depends(require_lead_access)
):
    return lead


# UPDATE lead (PUT)

@router.put(
    "/{lead_id}",
    response_model=schemas.LeadResponse
)
def update_lead(
    lead_id: int,
    lead: schemas.LeadCreate,
    db: Session = Depends(get_db),
    current_lead = Depends(require_admin)
):
    return service.update_lead(
        db,
        lead_id,
        lead
    )


# PATCH lead
@router.patch(
    "/{lead_id}",
    response_model=schemas.LeadResponse
)
def patch_lead(
    lead_id: int,
    lead: schemas.LeadUpdate,
    db: Session = Depends(get_db),
    current_lead = Depends(require_lead_access),
    _ = Depends(rate_limiter)
):
    return service.patch_lead(
        db,
        lead_id,
        lead
    )


# DELETE lead
@router.delete(
    "/{lead_id}",
    status_code=204
)
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    user = Depends(require_admin),
    _ = Depends(rate_limiter)
):
    service.delete_lead(
        db,
        lead_id
    )

    return None