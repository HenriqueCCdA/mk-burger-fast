import pytest
from fastapi import status

from app.main import app


@pytest.mark.integration
def test_status_list(client, status_list):

    response = client.get(app.url_path_for("list_status"))

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert len(body) == 2

    for r, e in zip(body, status_list):
        assert r["id"] is not None
        assert r["tipo"] == e.tipo


@pytest.mark.integration
def test_ingredients_list(client, ingredients):

    response = client.get(app.url_path_for("list_ingredients"))

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert len(body["paes"]) == 1
    assert len(body["carnes"]) == 2
    assert len(body["opcionais"]) == 1

    for r, e in zip(body["paes"], ingredients["breads"]):
        assert r["id"] is not None
        assert r["tipo"] == e.tipo

    for r, e in zip(body["carnes"], ingredients["meats"]):
        assert r["id"] is not None
        assert r["tipo"] == e.tipo

    for r, e in zip(body["opcionais"], ingredients["optionals"]):
        assert r["id"] is not None
        assert r["tipo"] == e.tipo
