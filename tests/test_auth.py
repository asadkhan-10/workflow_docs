import pytest
from fastapi import HTTPException, status
from app import oauth2
from app.oauth2 import verify_access_token


def get_credentials_exception():
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials"
    )


def test_unauthorized_access(client):
    res = client.get("/workflows")
    assert res.status_code == 401


def test_authorized_access(authorized_client):
    res = authorized_client.get("/workflows")
    assert res.status_code == 200


def test_token_contains_user_id(token, test_user):
    payload = verify_access_token(token, get_credentials_exception())
    assert payload.id == test_user["id"]


def test_invalid_token():
    invalid_token = "this.is.invalid.token"

    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(invalid_token, get_credentials_exception())

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_expired_token(test_user, monkeypatch):
    monkeypatch.setattr(oauth2, "ACCESS_TOKEN_EXPIRE_MINUTES", -1)

    expired_token = oauth2.create_access_token({"user_id": test_user["id"]})

    with pytest.raises(HTTPException) as exc_info:
        verify_access_token(expired_token, get_credentials_exception())

    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
