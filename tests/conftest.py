# tests/conftest.py
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app.oauth2 import create_access_token
from app import models

# test database URL — points to workflow_docs_test
SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:"
    f"{settings.database_password}@"
    f"{settings.database_hostname}:"
    f"{settings.database_port}/"
    f"{settings.database_name}_test"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "testuser@gmail.com",
        "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "testuser2@gmail.com",
        "password": "password123"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_workflows(test_user, session):
    workflows_data = [
        {
            "title": "First Workflow",
            "raw_input": "Send email when form is submitted",
            "input_type": "text",
            "owner_id": test_user["id"]
        },
        {
            "title": "Second Workflow",
            "raw_input": "Sync data between two systems",
            "input_type": "text",
            "owner_id": test_user["id"]
        },
        {
            "title": "Third Workflow",
            "raw_input": '{"nodes": [], "connections": {}}',
            "input_type": "json",
            "owner_id": test_user["id"]
        },
    ]

    def create_workflow_model(workflow):
        return models.Workflow(**workflow)

    workflows = list(map(create_workflow_model, workflows_data))
    session.add_all(workflows)
    session.commit()
    return session.query(models.Workflow).all()