def test_logistics_matching_fulfilled(client):
    response = client.post(
        "/api/v1/logistics/match",
        json={
            "id": "B002",
            "name": "Puducherry Hotel",
            "crop": "Tomato",
            "required_quantity": 400,
            "location": "Puducherry",
            "latitude": 11.9416,
            "longitude": 79.8083
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res = data["data"]
    assert res["status"] == "fulfilled"
    assert res["collected_quantity"] == 400
    assert res["shortage"] == 0
    assert len(res["farmers"]) > 0
    # First farmer should be nearest to Puducherry (Farmer E at Puducherry distance ~0 km)
    assert res["farmers"][0]["distance_km"] <= 1.0


def test_logistics_multi_farmer_allocation(client):
    # Request large quantity (e.g. 1200 kg) requiring multiple farmers
    response = client.post(
        "/api/v1/logistics/match",
        json={
            "id": "B003",
            "name": "Bulk Distribution Hub",
            "crop": "Tomato",
            "required_quantity": 1200,
            "location": "Puducherry",
            "latitude": 11.9416,
            "longitude": 79.8083
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    res = data["data"]
    assert res["collected_quantity"] >= 1000
    assert len(res["farmers"]) >= 2
    # Ensure sorted by distance ascending
    distances = [f["distance_km"] for f in res["farmers"]]
    assert distances == sorted(distances)
