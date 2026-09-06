def test_root_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["project"] == "FarmApp"


def test_db_health(client):
    response = client.get("/health/db")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"


def test_ai_health(client):
    response = client.get("/health/ai")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


def test_ai_chat_endpoint(client):
    response = client.post(
        "/api/v1/ai/chat",
        json={
            "message": "What fresh tomatoes do you have today from local farmers?"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    chat_data = data["data"]
    assert "response" in chat_data
    assert len(chat_data["response"]) > 0
    assert chat_data["role"] == "assistant"
