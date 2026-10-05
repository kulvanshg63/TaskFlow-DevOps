import pytest

from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200


def test_add_task(client):
    response = client.post(
        "/add",
        data={
            "title": "Test Task",
            "description": "Testing TaskFlow"
        },
        follow_redirects=True
    )

    assert response.status_code == 200