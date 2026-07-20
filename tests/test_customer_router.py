import uuid

from app.main import app

from app.core.permissions import (
    require_agent,
    require_admin
)

from app.core.rate_limit import rate_limiter

from app.users.models import User
from app.customers.models import Customer
from app.properties.models import Property
from app.leads.models import Lead
from fastapi import HTTPException


# -------------------------------------------------------
# Helper
# -------------------------------------------------------

def create_customer_test_data(db):

    unique = str(uuid.uuid4())[:8]


    agent = User(
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


    db.add_all([
        agent,
        admin,
        customer,
        property
    ])

    db.commit()


    db.refresh(agent)
    db.refresh(admin)
    db.refresh(customer)
    db.refresh(property)


    return agent, admin, customer, property



# -------------------------------------------------------
# GET ALL CUSTOMERS
# -------------------------------------------------------

def test_get_all_customers(client, db):

    agent, _, _, _ = create_customer_test_data(db)


    app.dependency_overrides[require_agent] = lambda: agent


    response = client.get("/customers/")


    assert response.status_code == 200


    data = response.json()

    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "data" in data



# -------------------------------------------------------
# CREATE CUSTOMER
# -------------------------------------------------------

def test_create_customer(client, db):

    agent, _, _, _ = create_customer_test_data(db)


    app.dependency_overrides[require_agent] = lambda: agent


    response = client.post(
        "/customers/",
        json={
            "name": "Ali",
            "email": "ali@test.com",
            "phone": "03001111111",
            "status": "active"
        }
    )


    assert response.status_code == 201


    data = response.json()

    assert data["name"] == "Ali"
    assert data["email"] == "ali@test.com"



# -------------------------------------------------------
# GET CUSTOMER BY ID
# -------------------------------------------------------

def test_get_customer_by_id(client, db):

    agent, _, customer, _ = create_customer_test_data(db)


    app.dependency_overrides[require_agent] = lambda: agent


    response = client.get(
        f"/customers/{customer.id}"
    )


    assert response.status_code == 200


    assert response.json()["id"] == customer.id



# -------------------------------------------------------
# UPDATE CUSTOMER
# -------------------------------------------------------

def test_update_customer(client, db):

    agent, _, customer, _ = create_customer_test_data(db)


    app.dependency_overrides[require_agent] = lambda: agent


    response = client.put(
        f"/customers/{customer.id}",
        json={
            "name": "Updated Customer",
            "email": customer.email,
            "phone": "03009999999",
            "status": "active"
        }
    )


    assert response.status_code == 200


    assert response.json()["name"] == "Updated Customer"



# -------------------------------------------------------
# PATCH CUSTOMER
# -------------------------------------------------------

def test_patch_customer(client, db):

    agent, _, customer, _ = create_customer_test_data(db)


    app.dependency_overrides[require_agent] = lambda: agent


    response = client.patch(
        f"/customers/{customer.id}",
        json={
            "status": "inactive"
        }
    )


    assert response.status_code == 200


    assert response.json()["status"] == "inactive"



# -------------------------------------------------------
# CUSTOMER NOT FOUND - GET
# -------------------------------------------------------

def test_get_customer_not_found(client, db):

    agent, _, _, _ = create_customer_test_data(db)


    app.dependency_overrides[require_agent] = lambda: agent


    response = client.get(
        "/customers/99999"
    )


    assert response.status_code == 404



# -------------------------------------------------------
# CUSTOMER NOT FOUND - UPDATE
# -------------------------------------------------------

def test_update_customer_not_found(client, db):

    agent, _, _, _ = create_customer_test_data(db)


    app.dependency_overrides[require_agent] = lambda: agent


    response = client.put(
        "/customers/99999",
        json={
            "name": "Missing",
            "email": "missing@test.com",
            "phone": "03000000000",
            "status": "active"
        }
    )


    assert response.status_code == 404



# -------------------------------------------------------
# CUSTOMER NOT FOUND - DELETE
# -------------------------------------------------------

def test_delete_customer_not_found(client, db):

    admin = User(
        username="admin_test",
        hashed_password="password",
        role="admin"
    )

    db.add(admin)
    db.commit()

    db.refresh(admin)


    app.dependency_overrides[require_admin] = lambda: admin


    response = client.delete(
        "/customers/99999"
    )


    assert response.status_code == 404



# -------------------------------------------------------
# PERMISSION DENIED
# Agent cannot delete
# -------------------------------------------------------

def test_customer_delete_permission_denied(client, db):

    _, _, customer, _ = create_customer_test_data(db)

    def fake_admin():
        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )

    app.dependency_overrides[require_admin] = fake_admin

    response = client.delete(
        f"/customers/{customer.id}"
    )

    assert response.status_code == 403

    app.dependency_overrides.pop(require_admin, None)


# -------------------------------------------------------
# BUSINESS RULE
# Cannot delete customer with active leads
# -------------------------------------------------------

def test_delete_customer_with_active_leads(client, db):

    agent, admin, customer, property = create_customer_test_data(db)


    lead = Lead(
        status="new",
        property_id=property.id,
        customer_id=customer.id,
        agent_id=agent.id
    )


    db.add(lead)

    db.commit()


    app.dependency_overrides[require_admin] = lambda: admin


    response = client.delete(
        f"/customers/{customer.id}"
    )


    assert response.status_code == 409