def test_root(client):
    response = client.get("/")

    assert response.status_code == 200


def test_get_users(client):
    response = client.get("/users")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user_validation(client):
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "invalid-test@example.com"
        }
    )

    assert response.status_code == 422


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "name": "Pytest User",
            "email": "pytest-user@example.com",
            "password": "Test123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Pytest User"
    assert data["email"] == "pytest-user@example.com"
    assert "password" not in data


def test_login(client):
    client.post(
        "/users",
        json={
            "name": "Login Test User",
            "email": "login-test@example.com",
            "password": "Test123456"
        }
    )

    response = client.post(
        "/login",
        json={
            "email": "login-test@example.com",
            "password": "Test123456"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_current_user(client):
    client.post(
        "/users",
        json={
            "name": "Me Test User",
            "email": "me-test@example.com",
            "password": "Test123456"
        }
    )

    login_response = client.post(
        "/login",
        json={
            "email": "me-test@example.com",
            "password": "Test123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Me Test User"
    assert data["email"] == "me-test@example.com"


def test_current_user_without_token(client):
    response = client.get("/users/me")

    assert response.status_code == 401


def test_login_wrong_password(client):
    client.post(
        "/users",
        json={
            "name": "Wrong Password User",
            "email": "wrong-password@example.com",
            "password": "Correct123456"
        }
    )

    response = client.post(
        "/login",
        json={
            "email": "wrong-password@example.com",
            "password": "Wrong123456"
        }
    )

    assert response.status_code == 401


def test_update_other_user_forbidden(client):
    first_user = client.post(
        "/users",
        json={
            "name": "User One",
            "email": "user-one@example.com",
            "password": "Test123456"
        }
    ).json()

    second_user = client.post(
        "/users",
        json={
            "name": "User Two",
            "email": "user-two@example.com",
            "password": "Test123456"
        }
    ).json()

    login_response = client.post(
        "/login",
        json={
            "email": "user-one@example.com",
            "password": "Test123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.put(
        f"/users/{second_user['id']}",
        json={
            "name": "Hacked User",
            "email": "hacked@example.com",
            "password": "Test123456"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403

def test_update_own_user(client):
    user = client.post(
        "/users",
        json={
            "name": "Update Test User",
            "email": "update-test@example.com",
            "password": "Test123456"
        }
    ).json()

    login_response = client.post(
        "/login",
        json={
            "email": "update-test@example.com",
            "password": "Test123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.put(
        f"/users/{user['id']}",
        json={
            "name": "Updated User",
            "email": "updated-user@example.com",
            "password": "NewPassword123"
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Updated User"
    assert data["email"] == "updated-user@example.com"
    assert "password" not in data

def test_delete_other_user_forbidden(client):
    first_user = client.post(
        "/users",
        json={
            "name": "Delete User One",
            "email": "delete-user-one@example.com",
            "password": "Test123456"
        }
    ).json()

    second_user = client.post(
        "/users",
        json={
            "name": "Delete User Two",
            "email": "delete-user-two@example.com",
            "password": "Test123456"
        }
    ).json()

    login_response = client.post(
        "/login",
        json={
            "email": "delete-user-one@example.com",
            "password": "Test123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        f"/users/{second_user['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 403

def test_delete_own_user(client):
    user = client.post(
        "/users",
        json={
            "name": "Delete Test User",
            "email": "delete-test@example.com",
            "password": "Test123456"
        }
    ).json()

    login_response = client.post(
        "/login",
        json={
            "email": "delete-test@example.com",
            "password": "Test123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.delete(
        f"/users/{user['id']}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

def test_logout(client):
    client.post(
        "/users",
        json={
            "name": "Logout Test User",
            "email": "logout-test@example.com",
            "password": "Test123456"
        }
    )

    login_response = client.post(
        "/login",
        json={
            "email": "logout-test@example.com",
            "password": "Test123456"
        }
    )

    token = login_response.json()["access_token"]

    response = client.post(
        "/logout",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Logout successful"