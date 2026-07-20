from app.properties.schemas import PropertyCreate, PropertyUpdate

from app.properties.service import (
    create_property,
    get_property_by_id,
    get_all_properties,
    update_property,
    delete_property,
    patch_property,
)


def test_create_property_service(db):
    property_data = PropertyCreate(
        title="House",
        description="Nice house",
        price=5000000,
        location="Lahore",
        area=10,
        beds=4
    )

    result = create_property(db, property_data)

    assert result.id is not None
    assert result.title == "House"
    assert result.location == "Lahore"


def test_get_property_by_id(db):
    property_data = PropertyCreate(
        title="Villa",
        description="Luxury villa",
        price=12000000,
        location="Islamabad",
        area=20,
        beds=6
    )

    created = create_property(db, property_data)

    result = get_property_by_id(db, created.id)

    assert result is not None
    assert result.id == created.id
    assert result.title == "Villa"


def test_get_property_not_found(db):
    result = get_property_by_id(db, 999999)

    assert result is None


def test_get_all_properties(db):

    create_property(
        db,
        PropertyCreate(
            title="House A",
            description="A",
            price=1000000,
            location="Lahore",
            area=5,
            beds=2
        )
    )

    create_property(
        db,
        PropertyCreate(
            title="House B",
            description="B",
            price=2000000,
            location="Karachi",
            area=8,
            beds=3
        )
    )

    result = get_all_properties(db)

    assert result["total"] >= 2
    assert isinstance(result["data"], list)


def test_update_property(db):

    created = create_property(
        db,
        PropertyCreate(
            title="Old House",
            description="Old",
            price=4000000,
            location="Lahore",
            area=10,
            beds=3
        )
    )

    updated = update_property(
        db,
        created.id,
        PropertyUpdate(
            title="New House",
            description="Updated",
            price=6000000,
            location="Islamabad",
            area=12,
            beds=4
        )
    )

    assert updated.title == "New House"
    assert updated.price == 6000000
    assert updated.location == "Islamabad"


def test_update_property_not_found(db):

    result = update_property(
        db,
        999999,
        PropertyUpdate(
            title="Test",
            description="Test",
            price=1,
            location="Test",
            area=1,
            beds=1
        )
    )

    assert result is None


def test_patch_property(db):

    created = create_property(
        db,
        PropertyCreate(
            title="Patch Test",
            description="Description",
            price=3000000,
            location="Lahore",
            area=8,
            beds=2
        )
    )

    patched = patch_property(
        db,
        created.id,
        PropertyUpdate(
            price=7000000,
            beds=5
        )
    )

    assert patched.price == 7000000
    assert patched.beds == 5
    assert patched.title == "Patch Test"


def test_patch_property_not_found(db):

    result = patch_property(
        db,
        999999,
        PropertyUpdate(price=100)
    )

    assert result is None


def test_delete_property(db):

    created = create_property(
        db,
        PropertyCreate(
            title="Delete Test",
            description="Delete",
            price=2500000,
            location="Lahore",
            area=7,
            beds=2
        )
    )

    deleted = delete_property(db, created.id)

    assert deleted.id == created.id
    assert get_property_by_id(db, created.id) is None


def test_delete_property_not_found(db):

    result = delete_property(db, 999999)

    assert result is None


def test_create_property_business_rule_negative_price(db):

    property_data = PropertyCreate(
        title="Invalid House",
        description="Negative price",
        price=-500,
        location="Lahore",
        area=10,
        beds=3
    )

    result = create_property(db, property_data)

    assert result is None