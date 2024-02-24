from fastapi import status


def test_status_list(client, status_list):

    response = client.get("/status/")

    assert response.status_code == status.HTTP_200_OK

    body = response.json()

    assert len(body) == 2

    for r, e in zip(body, status_list):
        assert r["id"] is not None
        assert r["tipo"] == e.tipo
