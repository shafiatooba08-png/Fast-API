import hmac
import hashlib

from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    Header,
    Depends
)

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.leads import models as lead_models


router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"]
)


class WebhookPayload(BaseModel):
    customer_id: int
    property_id: int
    status: str


WEBHOOK_SECRET = "my_webhook_secret_123"


# Default agent for external webhook leads
DEFAULT_AGENT_ID = 1


@router.post("/inbound")
async def inbound_webhook(
    payload: WebhookPayload,
    request: Request,
    db: Session = Depends(get_db),
    x_webhook_signature: str | None = Header(default=None)
):

    signature = x_webhook_signature


    if signature is None:
        raise HTTPException(
            status_code=401,
            detail="Missing webhook signature"
        )


    body = await request.body()


    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        body,
        hashlib.sha256
    ).hexdigest()


    if not hmac.compare_digest(
        signature,
        expected_signature
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid webhook signature"
        )


    # Check existing lead
    existing_lead = db.query(
        lead_models.Lead
    ).filter(
        lead_models.Lead.customer_id == payload.customer_id,
        lead_models.Lead.property_id == payload.property_id
    ).first()


    # Update existing lead
    if existing_lead:

        existing_lead.status = payload.status

        db.commit()
        db.refresh(existing_lead)

        print(
            "WEBHOOK UPDATED LEAD:",
            existing_lead.id,
            existing_lead.status
        )


        return {
            "message": "Lead updated",
            "lead_id": existing_lead.id
        }


    # Create new lead
    new_lead = lead_models.Lead(
        customer_id=payload.customer_id,
        property_id=payload.property_id,
        status=payload.status,
        agent_id=DEFAULT_AGENT_ID
    )


    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)


    print(
        "WEBHOOK CREATED LEAD:",
        new_lead.id,
        new_lead.status
    )


    return {
        "message": "Lead created",
        "lead_id": new_lead.id
    }