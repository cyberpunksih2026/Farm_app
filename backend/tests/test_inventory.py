def test_get_inventory(client):
    response = client.get("/api/v1/inventory/product/1")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    inv = data["data"]
    assert inv["stock_quantity"] >= 500.0
    assert inv["available_quantity"] >= 500.0


def test_restock_employee_role(client, employee_headers, customer_headers):
    # Customer forbidden
    cust_res = client.post("/api/v1/inventory/product/1/restock", json={"quantity": 50.0}, headers=customer_headers)
    assert cust_res.status_code == 403

    # Employee allowed
    emp_res = client.post("/api/v1/inventory/product/1/restock", json={"quantity": 50.0}, headers=employee_headers)
    assert emp_res.status_code == 200
    assert emp_res.json()["data"]["stock_quantity"] >= 550.0
