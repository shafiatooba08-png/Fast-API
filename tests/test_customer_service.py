from app.customers.schemas import CustomerCreate, CustomerUpdate

from app.customers.service import (
    create_customer,
    get_customer_by_id,
    get_all_customers,
    update_customer,
    patch_customer,
    delete_customer,
)


def test_create_customer_service(db):

    customer_data = CustomerCreate(
        name="Ali Khan",
        email="ali@gmail.com",
        phone="03001234567"
    )

    result = create_customer(db, customer_data)

    assert result.id is not None
    assert result.name == "Ali Khan"
    assert result.email == "ali@gmail.com"



def test_get_customer_by_id(db):

    customer_data = CustomerCreate(
        name="Ahmed",
        email="ahmed@gmail.com",
        phone="03001111111"
    )

    created = create_customer(db, customer_data)

    result = get_customer_by_id(db, created.id)

    assert result is not None
    assert result.id == created.id
    assert result.name == "Ahmed"



def test_get_customer_not_found(db):

    result = get_customer_by_id(db, 999999)

    assert result is None



def test_get_all_customers(db):

    create_customer(
        db,
        CustomerCreate(
            name="Customer A",
            email="a@gmail.com",
            phone="03000000001"
        )
    )


    create_customer(
        db,
        CustomerCreate(
            name="Customer B",
            email="b@gmail.com",
            phone="03000000002"
        )
    )


    result = get_all_customers(db)

    assert result["total"] >= 2
    assert isinstance(result["data"], list)



def test_update_customer(db):

    created = create_customer(
        db,
        CustomerCreate(
            name="Old Name",
            email="old@gmail.com",
            phone="03000000003"
        )
    )


    updated = update_customer(
        db,
        created.id,
        CustomerUpdate(
            name="New Name",
            email="new@gmail.com",
            phone="03000000004"
        )
    )


    assert updated.name == "New Name"
    assert updated.email == "new@gmail.com"



def test_update_customer_not_found(db):

    result = update_customer(
        db,
        999999,
        CustomerUpdate(
            name="Test",
            email="test@gmail.com",
            phone="03000000000"
        )
    )


    assert result is None



def test_patch_customer(db):

    created = create_customer(
        db,
        CustomerCreate(
            name="Patch Test",
            email="patch@gmail.com",
            phone="03000000005"
        )
    )


    patched = patch_customer(
        db,
        created.id,
        CustomerUpdate(
            phone="03009999999"
        )
    )


    assert patched.phone == "03009999999"
    assert patched.name == "Patch Test"



def test_patch_customer_not_found(db):

    result = patch_customer(
        db,
        999999,
        CustomerUpdate(
            phone="03000000000"
        )
    )


    assert result is None



def test_delete_customer(db):

    created = create_customer(
        db,
        CustomerCreate(
            name="Delete Test",
            email="delete@gmail.com",
            phone="03000000006"
        )
    )


    deleted = delete_customer(db, created.id)


    assert deleted.id == created.id
    assert get_customer_by_id(db, created.id) is None



def test_delete_customer_not_found(db):

    result = delete_customer(db, 999999)

    assert result is None



def test_create_customer_business_rule_duplicate_email(db):

    create_customer(
        db,
        CustomerCreate(
            name="First Customer",
            email="same@gmail.com",
            phone="03000000007"
        )
    )


    result = create_customer(
        db,
        CustomerCreate(
            name="Second Customer",
            email="same@gmail.com",
            phone="03000000008"
        )
    )


    assert result is None