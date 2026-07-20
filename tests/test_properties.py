def test_get_properties(client):

    response = client.get("/properties/")

    assert response.status_code == 200

    data = response.json()

    assert "total" in data
    assert "page" in data
    assert "limit" in data
    assert "data" in data

    assert isinstance(
        data["data"],
        list
    )
    
    
def test_property_not_found(client):

    response = client.get("/properties/99999")

    assert response.status_code == 404