import pytest
from jose import jwt
from app import schemas

from app.config import settings


# def test_root(client):

#     res = client.get("/")
#     print(res.json().get('message'))
#     assert res.json().get('message') == 'Hello World'
#     assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_create_user_does_not_return_password(client):
    res = client.post(
        "/users/", json={"email": "nopassword@gmail.com", "password": "password123"}
    )

    assert "password" not in res.json()
    assert res.status_code == 201


def test_create_user_duplicate_email(client):
    user_data = {"email": "duplicate@gmail.com", "password": "password123"}

    first_res = client.post("/users/", json=user_data)
    second_res = client.post("/users/", json=user_data)

    assert first_res.status_code == 201
    assert second_res.status_code == 409
    assert second_res.json()["detail"] == "Email already registered"


def test_login_user(test_user, client):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.secret_key, algorithms=[settings.algorithm]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 403),
        ("sanjeev@gmail.com", "wrongpassword", 403),
        ("wrongemail@gmail.com", "wrongpassword", 403),
        (None, "password123", 422),
        ("sanjeev@gmail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    form_data = {}
    if email is not None:
        form_data["username"] = email
    if password is not None:
        form_data["password"] = password

    res = client.post("/login", data=form_data)
    assert res.status_code == status_code

# testing that one user (A) should not be able to delete the user (B)
def test_delete_user_unauthorized(client, test_user, test_user2):
    # login as user1
    res = client.post("/login", data={
        "username": test_user["email"],
        "password": test_user["password"]
    })
    token = res.json()["access_token"]

    client.headers = {"Authorization": f"Bearer {token}"}

    # try deleting user2
    res = client.delete(f"/users/{test_user2['id']}")
    assert res.status_code == 403


# deleting a user
def test_delete_user(authorized_client, test_user):
    res = authorized_client.delete(f"/users/{test_user['id']}")
    assert res.status_code == 204


#testing that you cant delete non-existing user 
def test_delete_user_not_found(authorized_client):
    res = authorized_client.delete("/users/9999")
    assert res.status_code == 404  
    
def test_delete_user_no_token(client, test_user):
    res = client.delete(f"/users/{test_user['id']}")
    assert res.status_code == 401
