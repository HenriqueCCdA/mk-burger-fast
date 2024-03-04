import pytest
from fastapi import status as status_

from app.main import app

URL_CREATE = app.url_path_for("create_burgers")


@pytest.mark.integration
def test_status_list(client, status_list):

    response = client.get(app.url_path_for("list_status"))

    assert response.status_code == status_.HTTP_200_OK

    body = response.json()

    assert len(body) == 2

    for r, e in zip(body, status_list):
        assert r["id"] is not None
        assert r["tipo"] == e.tipo


@pytest.mark.integration
def test_ingredients_list(client, ingredients):

    response = client.get(app.url_path_for("list_ingredients"))

    assert response.status_code == status_.HTTP_200_OK

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


@pytest.mark.integration
def test_list_burgers(client, burger_list):

    response = client.get(app.url_path_for("list_burgers"))

    assert response.status_code == status_.HTTP_200_OK

    body = response.json()

    assert len(body) == 2

    for e, r in zip(burger_list, body):
        assert e.id is not None
        assert e.name == r["nome"]


@pytest.mark.integration
def test_positive_create_burgers(client, payload_create):

    response = client.post(URL_CREATE, json=payload_create)

    assert response.status_code == status_.HTTP_201_CREATED

    body = response.json()

    assert body.pop("id") is not None
    assert body == {
        "nome": "João",
        "carne": "Alcatra",
        "pao": "Integral",
        "status": "Solicitado",
        "opcionais": ["Cebola roxa", "Bacon"],
    }


@pytest.mark.integration
def test_positive_create_burgers_meat_wrong_id(client, payload_create):

    wrong_id = payload_create["carne"] + 1
    payload_create["carne"] = wrong_id

    response = client.post(URL_CREATE, json=payload_create)

    assert response.status_code == status_.HTTP_422_UNPROCESSABLE_ENTITY

    body = response.json()

    assert body == {"detail": f"Carne com id '{wrong_id}' não existe."}


@pytest.mark.integration
def test_positive_create_burgers_bread_wrong_id(client, payload_create):

    wrong_id = payload_create["pao"] + 1
    payload_create["pao"] = wrong_id

    response = client.post(URL_CREATE, json=payload_create)

    assert response.status_code == status_.HTTP_422_UNPROCESSABLE_ENTITY

    body = response.json()

    assert body == {"detail": f"Pao com id '{wrong_id}' não existe."}


@pytest.mark.integration
def test_positive_create_burgers_status_wrong_id(client, payload_create):

    wrong_id = payload_create["status"] + 1
    payload_create["status"] = wrong_id

    response = client.post(URL_CREATE, json=payload_create)

    assert response.status_code == status_.HTTP_422_UNPROCESSABLE_ENTITY

    body = response.json()

    assert body == {"detail": f"Status com id '{wrong_id}' não existe."}


@pytest.mark.integration
def test_positive_create_burgers_optional_wrong_id(client, payload_create):

    payload_create["opcionais"] = [404]

    response = client.post(URL_CREATE, json=payload_create)

    assert response.status_code == status_.HTTP_422_UNPROCESSABLE_ENTITY

    body = response.json()

    assert body == {"detail": "Opcional com id '404' não existe."}
