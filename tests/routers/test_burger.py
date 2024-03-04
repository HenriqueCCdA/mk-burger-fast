import pytest
from fastapi import status
from sqlalchemy import select

from app.main import app
from app.models import Burger

URL_CREATE_BURGER = app.url_path_for("create_burger")


@pytest.mark.integration
def test_list_burgers(client, burger_list):

    response = client.get(app.url_path_for("list_burgers"))

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert len(body) == 2

    for e, r in zip(burger_list, body):
        assert e.id is not None
        assert e.name == r["nome"]


@pytest.mark.integration
def test_positive_create_burgers(client, payload_create):

    response = client.post(URL_CREATE_BURGER, json=payload_create)
    assert response.status_code == status.HTTP_201_CREATED

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

    response = client.post(URL_CREATE_BURGER, json=payload_create)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    body = response.json()

    assert body == {"detail": f"Carne com id '{wrong_id}' não existe."}


@pytest.mark.integration
def test_positive_create_burgers_bread_wrong_id(client, payload_create):

    wrong_id = payload_create["pao"] + 1
    payload_create["pao"] = wrong_id

    response = client.post(URL_CREATE_BURGER, json=payload_create)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    body = response.json()

    assert body == {"detail": f"Pao com id '{wrong_id}' não existe."}


@pytest.mark.integration
def test_positive_create_burgers_status_wrong_id(client, payload_create):

    wrong_id = payload_create["status"] + 1
    payload_create["status"] = wrong_id

    response = client.post(URL_CREATE_BURGER, json=payload_create)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    body = response.json()

    assert body == {"detail": f"Status com id '{wrong_id}' não existe."}


@pytest.mark.integration
def test_positive_create_burgers_optional_wrong_id(client, payload_create):

    payload_create["opcionais"] = [404]

    response = client.post(URL_CREATE_BURGER, json=payload_create)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    body = response.json()

    assert body == {"detail": "Opcional com id '404' não existe."}


@pytest.mark.integration
def test_positive_delete_burger(client, session, burger_db):

    url = app.url_path_for("delele_burger", id=burger_db.id)

    response = client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert not session.scalar(select(Burger).where(Burger.id == burger_db.id))


@pytest.mark.integration
def test_negative_delete_burger_not_found(client):

    url = app.url_path_for("delele_burger", id=404)

    response = client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    body = response.json()

    assert body == {"detail": "Buger não achado"}
