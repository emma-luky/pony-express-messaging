from fastapi.testclient import TestClient
from backend.main import app

def test_get_all_users():
    client = TestClient(app)
    response = client.get("/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])

def test_create_user_success():
    create_params = {
        "id": "new_user_id"
    }

    client = TestClient(app)
    response = client.post("/users", json=create_params)

    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    user = data["user"]
    for key, value in create_params.items():
        assert user[key] == value

    response = client.get(f"/users/{user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    user = data["user"]
    for key, value in create_params.items():
        assert user[key] == value

def test_create_user_fail():
    create_params = {
        "id": "sarah"
    }

    client = TestClient(app)
    response = client.post("/users", json=create_params)
    assert response.status_code == 422

    assert response.json() == {
        "detail": {
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": "sarah"
        }
    }

def test_get_user_by_id_success():
    client = TestClient(app)
    response = client.get("/users/sarah")
    assert response.status_code == 200

    user = response.json()["user"]
    assert user["id"] == "sarah"
    assert user["created_at"] == "2006-03-02T22:30:11"

def test_get_user_by_id_fail():
    client = TestClient(app)
    response = client.get("/users/1")
    assert response.status_code == 404

    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": "1"
        }
    }

def test_get_user_chats_success():
    client = TestClient(app)
    response = client.get("/users/sarah/chats")
    assert response.status_code == 200

    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])

def test_get_user_chats_fail():
    client = TestClient(app)
    response = client.get("/users/1/chats")
    assert response.status_code == 404

    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": "1"
        }
    }