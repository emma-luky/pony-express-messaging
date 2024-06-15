from fastapi.testclient import TestClient
from backend.main import app

def test_get_all_chats():
    client = TestClient(app)
    response = client.get("/chats")
    assert response.status_code == 200

    meta = response.json()["meta"]
    chats = response.json()["chats"]
    assert meta["count"] == len(chats)
    assert chats == sorted(chats, key=lambda chat: chat["name"])

def test_get_chat_by_id_success():
    client = TestClient(app)
    response = client.get("/chats/6215e6864e884132baa01f7f972400e2")
    assert response.status_code == 200

    chat = response.json()["chat"]
    assert chat["id"] == "6215e6864e884132baa01f7f972400e2"
    assert chat["name"] == "skynet"
    assert chat["user_ids"] == ["sarah", "terminator"]
    assert chat["owner_id"] == "sarah"
    assert chat["created_at"] == "2023-07-08T18:46:47"

def test_get_chat_by_id_fail():
    client = TestClient(app)
    response = client.get("/chats/1")
    assert response.status_code == 404

    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "1"
        }
    }

def test_update_chat_success():
    update_params = {
        "name": "updated_chat_name"
    }

    expected_chat = {
        "id": "6215e6864e884132baa01f7f972400e2",
        "name": update_params["name"],
        "user_ids": ["sarah", "terminator"],
        "owner_id": "sarah",
        "created_at": "2023-07-08T18:46:47",
    }
    client = TestClient(app)
    response = client.put("/chats/6215e6864e884132baa01f7f972400e2", json=update_params)
    assert response.status_code == 200
    assert response.json() == {"chat": expected_chat}

    # test that the update is persisted
    response = client.get("/chats/6215e6864e884132baa01f7f972400e2")
    assert response.status_code == 200
    assert response.json() == {"chat": expected_chat}

def test_update_chat_fail():
    update_params = {
        "name": "updated_chat_name"
    }

    client = TestClient(app)
    response = client.put("/chats/1", json=update_params)
    assert response.status_code == 404

    detail = response.json()["detail"]
    assert detail["type"] == "entity_not_found"
    assert detail["entity_name"] == "Chat"
    assert detail["entity_id"] == "1"

def test_delete_chat_success():
    client = TestClient(app)
    response = client.delete("/chats/6215e6864e884132baa01f7f972400e2")

    assert response.status_code == 204

def test_delete_chat_fail():
    client = TestClient(app)
    response = client.delete("/chats/1")
    assert response.status_code == 404

    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "1"
        }
    }

def test_get_chat_messages_success():
    client = TestClient(app)
    response = client.get("/chats/6215e6864e884132baa01f7f972400e2/messages")
    assert response.status_code == 200

    meta = response.json()["meta"]
    messages = response.json()["messages"]
    assert meta["count"] == len(messages)
    assert messages == sorted(messages, key=lambda message: message["created_at"])


def test_get_chat_messages_fail():
    client = TestClient(app)
    response = client.get("/chats/1/messages")
    assert response.status_code == 404

    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "1"
        }
    }

def test_get_chat_users_success():
    client = TestClient(app)
    response = client.get("/chats/6215e6864e884132baa01f7f972400e2/users")
    assert response.status_code == 200

    meta = response.json()["meta"]
    users = response.json()["users"]
    assert meta["count"] == len(users)
    assert users == sorted(users, key=lambda user: user["id"])

def test_get_chat_users_fail():
    client = TestClient(app)
    response = client.get("/chats/1/users")
    assert response.status_code == 404

    assert response.json() == {
        "detail": {
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": "1"
        }
    }