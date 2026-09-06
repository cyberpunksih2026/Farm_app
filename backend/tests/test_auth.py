def test_login_success(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username_or_email_phone": "ishanrajavelu75@gmail.com",
            "password": "Admin@123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]
    assert data["data"]["user"]["role"] == "ADMIN"


def test_login_invalid_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "username_or_email_phone": "ishanrajavelu75@gmail.com",
            "password": "WrongPassword@999"
        }
    )
    assert response.status_code == 401
    assert response.json()["success"] is False


def test_customer_registration(client):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test Farm Customer",
            "email": "newcustomer@farmapp.in",
            "phone": "9876500001",
            "password": "CustomerPass@123",
            "username": "testcustomer1"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["user"]["email"] == "newcustomer@farmapp.in"
    assert data["data"]["user"]["role"] == "CUSTOMER"


def test_get_me_authenticated(client, customer_headers):
    response = client.get("/api/v1/auth/me", headers=customer_headers)
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_get_me_unauthorized(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
