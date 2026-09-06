def test_cart_operations(client, customer_headers):
    # 1. Add item to cart
    add_res = client.post(
        "/api/v1/cart/items",
        json={"product_id": 1, "quantity": 2.0},
        headers=customer_headers
    )
    assert add_res.status_code == 201
    cart = add_res.json()["data"]
    assert len(cart["items"]) == 1
    assert cart["subtotal"] > 0
    assert cart["farmer_total"] > 0
    assert cart["market_total"] > cart["subtotal"]
    assert cart["savings"] > 0

    item_id = cart["items"][0]["id"]

    # 2. Update item quantity
    upd_res = client.put(
        f"/api/v1/cart/items/{item_id}",
        json={"quantity": 3.0},
        headers=customer_headers
    )
    assert upd_res.status_code == 200
    assert upd_res.json()["data"]["items"][0]["quantity"] == 3.0

    # 3. Clear cart
    clear_res = client.delete("/api/v1/cart", headers=customer_headers)
    assert clear_res.status_code == 200


def test_order_checkout_and_lifecycle(client, customer_headers, admin_headers):
    # 1. Place order with direct items
    order_res = client.post(
        "/api/v1/orders",
        json={
            "items": [{"product_id": 1, "quantity": 2.0}],
            "payment_method": "UPI",
            "notes": "Please leave at front door"
        },
        headers=customer_headers
    )
    assert order_res.status_code == 201
    order = order_res.json()["data"]
    assert order["status"] == "CREATED"
    assert order["total_amount"] > 0
    order_id = order["id"]

    # 2. Transition state: CREATED -> CONFIRMED
    conf_res = client.patch(
        f"/api/v1/orders/{order_id}/status",
        json={"status": "CONFIRMED", "notes": "Order payment verified"},
        headers=admin_headers
    )
    assert conf_res.status_code == 200
    assert conf_res.json()["data"]["status"] == "CONFIRMED"

    # 3. Transition state: CONFIRMED -> PICKING -> PACKED -> READY_FOR_DISPATCH -> OUT_FOR_DELIVERY -> DELIVERED
    for next_status in ["PICKING", "PACKED", "READY_FOR_DISPATCH", "OUT_FOR_DELIVERY", "DELIVERED"]:
        step_res = client.patch(
            f"/api/v1/orders/{order_id}/status",
            json={"status": next_status},
            headers=admin_headers
        )
        assert step_res.status_code == 200
        assert step_res.json()["data"]["status"] == next_status

    # 4. Invalid state transition: DELIVERED -> CREATED should fail
    inv_res = client.patch(
        f"/api/v1/orders/{order_id}/status",
        json={"status": "CREATED"},
        headers=admin_headers
    )
    assert inv_res.status_code == 400
