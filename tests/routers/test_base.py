import pytest
from app.main import app
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)


@pytest.mark.integration
def test_home():
    resp = client.get("/")
    assert resp.status_code == status.HTTP_200_OK
