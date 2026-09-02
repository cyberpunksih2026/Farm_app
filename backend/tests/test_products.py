def test_list_products(client):
    response = client.get("/api/v1/products")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert len(data["data"]) > 0


def test_search_products(client):
    response = client.get("/api/v1/products?query=tomato")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    for item in data["data"]:
        assert "tomato" in item["name"].lower() or "tomato" in item["slug"].lower()


def test_filter_products_by_category(client):
    response = client.get("/api/v1/products?category=vegetables")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_product_detail_and_price_transparency(client):
    response = client.get("/api/v1/products/slug/country-vine-tomatoes")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    prod = data["data"]
    assert prod["farmer_price"] > 0
    assert prod["base_price"] > prod["farmer_price"]
    assert prod["farmer"] is not None
    assert prod["farmer"]["name"] == "Farmer A"
    assert prod["farmer"]["location"] == "Villupuram"


def test_create_product_admin_only(client, admin_headers, customer_headers):
    payload = {
        "farmer_id": 1,
        "category_id": 1,
        "name": "Fresh Organic Carrots",
        "slug": "fresh-organic-carrots",
        "description": "Crisp farm carrots",
        "unit": "kg",
        "base_price": 40.0,
        "farmer_price": 32.0,
        "market_price": 55.0,
        "initial_stock": 200.0,
        "is_organic": True
    }

    # Customer forbidden
    cust_res = client.post("/api/v1/products", json=payload, headers=customer_headers)
    assert cust_res.status_code == 403

    # Admin allowed
    admin_res = client.post("/api/v1/products", json=payload, headers=admin_headers)
    assert admin_res.status_code == 201
    assert admin_res.json()["data"]["name"] == "Fresh Organic Carrots"
