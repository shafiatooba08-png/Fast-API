from app.leads.service import (
    create_lead,
    get_lead_by_id,
    get_all_leads,
    update_lead,
    patch_lead,
    delete_lead
)

from app.leads.schemas import (
    LeadCreate,
    LeadUpdate
)

from app.properties.models import Property
from app.customers.models import Customer
from app.users.models import User

import pytest
import uuid


# helper function

def create_test_data(db):

    unique_id = str(uuid.uuid4())[:8]

    user = User(
        username=f"agent_{unique_id}",
        hashed_password="testpassword",
        role="agent"
    )

    customer = Customer(
        name=f"Test Customer {unique_id}",
        email=f"customer_{unique_id}@test.com",
        phone="123456789",
        status="active"
    )

    property = Property(
        title=f"Test Property {unique_id}",
        description="Test description",
        price=50000,
        location="Lahore",
        area=1200
    )

    db.add(user)
    db.add(customer)
    db.add(property)

    db.commit()

    db.refresh(user)
    db.refresh(customer)
    db.refresh(property)

    return user, customer, property



# CREATE lead

def test_create_lead_service(db):

    user, customer, property = create_test_data(db)

    lead_data = LeadCreate(
        status="new",
        property_id=property.id,
        customer_id=customer.id
    )

    lead = create_lead(
        db,
        lead_data,
        user
    )

    assert lead.id is not None
    assert lead.status == "new"
    assert lead.agent_id == user.id



# GET lead by id

def test_get_lead_by_id(db):

    user, customer, property = create_test_data(db)

    lead = create_lead(
        db,
        LeadCreate(
            status="new",
            property_id=property.id,
            customer_id=customer.id
        ),
        user
    )

    result = get_lead_by_id(
        db,
        lead.id
    )

    assert result.id == lead.id
    assert result.customer.id == customer.id
    assert result.property.id == property.id



# GET lead not found

def test_get_lead_not_found(db):

    from app.core.exceptions import LeadNotFoundError

    with pytest.raises(LeadNotFoundError):

        get_lead_by_id(
            db,
            9999
        )



# GET ALL leads

def test_get_all_leads(db):

    user, customer, property = create_test_data(db)

    create_lead(
        db,
        LeadCreate(
            status="new",
            property_id=property.id,
            customer_id=customer.id
        ),
        user
    )

    result = get_all_leads(
        db,
        page=1,
        limit=10
    )

    assert result["total"] >= 1
    assert len(result["data"]) >= 1



# UPDATE lead

def test_update_lead(db):

    user, customer, property = create_test_data(db)

    lead = create_lead(
        db,
        LeadCreate(
            status="new",
            property_id=property.id,
            customer_id=customer.id
        ),
        user
    )


    updated = update_lead(
        db,
        lead.id,
        LeadCreate(
            status="qualified",
            property_id=property.id,
            customer_id=customer.id
        )
    )


    assert updated.status == "qualified"



# UPDATE not found

def test_update_lead_not_found(db):

    from app.core.exceptions import LeadNotFoundError

    with pytest.raises(LeadNotFoundError):

        update_lead(
            db,
            9999,
            LeadCreate(
                status="new",
                property_id=1,
                customer_id=1
            )
        )



# PATCH lead

def test_patch_lead(db):

    user, customer, property = create_test_data(db)


    lead = create_lead(
        db,
        LeadCreate(
            status="new",
            property_id=property.id,
            customer_id=customer.id
        ),
        user
    )


    updated = patch_lead(
        db,
        lead.id,
        LeadUpdate(
            status="interested"
        )
    )


    assert updated.status == "interested"



# PATCH not found

def test_patch_lead_not_found(db):

    from app.core.exceptions import LeadNotFoundError


    with pytest.raises(LeadNotFoundError):

        patch_lead(
            db,
            9999,
            LeadUpdate(
                status="qualified"
            )
        )



# DELETE lead

def test_delete_lead(db):

    user, customer, property = create_test_data(db)


    lead = create_lead(
        db,
        LeadCreate(
            status="new",
            property_id=property.id,
            customer_id=customer.id
        ),
        user
    )


    deleted = delete_lead(
        db,
        lead.id
    )


    assert deleted.id == lead.id



# DELETE not found

def test_delete_lead_not_found(db):

    from app.core.exceptions import LeadNotFoundError


    with pytest.raises(LeadNotFoundError):

        delete_lead(
            db,
            9999
        )
# PERMISSION DENIED
# Agent cannot see another agent's leads

def test_agent_cannot_see_other_agent_leads(db):

    unique_id = str(uuid.uuid4())[:8]

    agent1 = User(
        username=f"agent_one_{unique_id}",
        hashed_password="password",
        role="agent"
    )

    agent2 = User(
        username=f"agent_two_{unique_id}",
        hashed_password="password",
        role="agent"
    )

    customer = Customer(
        name=f"Customer {unique_id}",
        email=f"customer_{unique_id}@test.com",
        phone="123456789",
        status="active"
    )

    property = Property(
        title=f"Property {unique_id}",
        description="Test property",
        price=100000,
        location="Lahore",
        area=1200
    )


    db.add_all([
        agent1,
        agent2,
        customer,
        property
    ])

    db.commit()


    db.refresh(agent1)
    db.refresh(agent2)
    db.refresh(customer)
    db.refresh(property)



    # Agent 1 creates lead

    create_lead(
        db,
        LeadCreate(
            status="new",
            property_id=property.id,
            customer_id=customer.id
        ),
        agent1
    )


    # Agent 2 tries to see leads

    result = get_all_leads(
        db,
        page=1,
        limit=10,
        user=agent2
    )


    assert result["total"] == 0
    assert len(result["data"]) == 0