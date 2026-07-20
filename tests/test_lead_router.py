import uuid

from fastapi.testclient import TestClient

from app.main import app
from app.leads.router import get_db
from app.core.permissions import require_agent, require_admin
from app.core.lead_permissions import require_lead_access
from app.core.rate_limit import rate_limiter

from app.users.models import User
from app.customers.models import Customer
from app.properties.models import Property
from app.leads.models import Lead


# ------------------------------------------------------------------
# Helper
# ------------------------------------------------------------------

def create_test_data(db):
    unique = str(uuid.uuid4())[:8]

    user = User(
        username=f"agent_{unique}",
        hashed_password="password",
        role="agent"
    )

    admin = User(
        username=f"admin_{unique}",
        hashed_password="password",
        role="admin"
    )

    customer = Customer(
        name="Test Customer",
        email=f"{unique}@test.com",
        phone="03001234567",
        status="active"
    )

    property = Property(
        title="House",
        description="Nice house",
        price=5000000,
        location="Lahore",
        area=10,
        beds=4
    )

    db.add_all([user, admin, customer, property])
    db.commit()

    db.refresh(user)
    db.refresh(admin)
    db.refresh(customer)
    db.refresh(property)

    lead = Lead(
        status="new",
        property_id=property.id,
        customer_id=customer.id,
        agent_id=user.id
    )

    db.add(lead)
    db.commit()
    db.refresh(lead)

    return user, admin, customer, property, lead


# ------------------------------------------------------------------
# GET ALL LEADS
# ------------------------------------------------------------------

def test_get_all_leads(client, db):

    user, _, _, _, _ = create_test_data(db)

    app.dependency_overrides[require_agent] = lambda: user
    app.dependency_overrides[rate_limiter] = lambda: None

    response = client.get("/leads/")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "data" in data


# ------------------------------------------------------------------
# CREATE LEAD
# ------------------------------------------------------------------

def test_create_lead(client, db):

    user, _, customer, property, _ = create_test_data(db)

    app.dependency_overrides[require_agent] = lambda: user
    app.dependency_overrides[rate_limiter] = lambda: None

    response = client.post(
        "/leads/",
        json={
            "status": "qualified",
            "property_id": property.id,
            "customer_id": customer.id
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["status"] == "qualified"
    assert data["agent_id"] == user.id


# ------------------------------------------------------------------
# GET LEAD BY ID
# ------------------------------------------------------------------

def test_get_lead_by_id(client, db):

    user, _, _, _, lead = create_test_data(db)

    app.dependency_overrides[require_lead_access] = lambda: lead

    response = client.get(f"/leads/{lead.id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == lead.id


# ------------------------------------------------------------------
# GET LEAD NOT FOUND
# ------------------------------------------------------------------

def test_get_lead_not_found(client):

    from fastapi import HTTPException

    def fake():
        raise HTTPException(
            status_code=404,
            detail="Lead not found"
        )

    app.dependency_overrides[require_lead_access] = fake

    response = client.get("/leads/99999")

    assert response.status_code == 404


# ------------------------------------------------------------------
# UPDATE LEAD
# ------------------------------------------------------------------

def test_update_lead(client, db):

    _, admin, customer, property, lead = create_test_data(db)

    app.dependency_overrides[require_admin] = lambda: admin

    response = client.put(
        f"/leads/{lead.id}",
        json={
            "status": "qualified",
            "property_id": property.id,
            "customer_id": customer.id
        }
    )

    assert response.status_code == 200

    assert response.json()["status"] == "qualified"


# ------------------------------------------------------------------
# PATCH LEAD
# ------------------------------------------------------------------

def test_patch_lead(client, db):

    user, _, _, _, lead = create_test_data(db)

    app.dependency_overrides[require_lead_access] = lambda: lead
    app.dependency_overrides[rate_limiter] = lambda: None

    response = client.patch(
        f"/leads/{lead.id}",
        json={
            "status": "interested"
        }
    )

    assert response.status_code == 200

    assert response.json()["status"] == "interested"


# ------------------------------------------------------------------
# DELETE LEAD
# ------------------------------------------------------------------

def test_delete_lead(client, db):

    _, admin, _, _, lead = create_test_data(db)

    app.dependency_overrides[require_admin] = lambda: admin
    app.dependency_overrides[rate_limiter] = lambda: None

    response = client.delete(f"/leads/{lead.id}")

    assert response.status_code == 204


# ------------------------------------------------------------------
# PERMISSION DENIED
# ------------------------------------------------------------------

def test_permission_denied(client):

    from fastapi import HTTPException

    def fake():
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    app.dependency_overrides[require_agent] = fake

    response = client.get("/leads/")

    assert response.status_code == 403


# ------------------------------------------------------------------
# BUSINESS RULE VIOLATION
# ------------------------------------------------------------------

def test_create_lead_invalid_customer(client, db):

    user, _, _, property, _ = create_test_data(db)

    app.dependency_overrides[require_agent] = lambda: user
    app.dependency_overrides[rate_limiter] = lambda: None

    response = client.post(
        "/leads/",
        json={
            "status": "new",
            "property_id": property.id,
            "customer_id": 999999
        }
    )

    assert response.status_code >= 400