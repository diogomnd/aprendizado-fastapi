from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_html_deve_retornar_o_texto_da_pagina(client):
    response = client.get("/html")

    assert (
        response.text
        == """
    <html>
        <head>
            <title> Nosso olá mundo </title>
         </head>
        <body>
            <h1>Algo diferente de olá mundo</h1>
        </body>
    </html>
    """
    )


def test_create_user(client):
    response = client.post(
        "/users",
        json={
            "username": "diogo",
            "email": "diogo@ufpb.com",
            "password": "diogo123",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "diogo",
        "email": "diogo@ufpb.com",
    }


def test_read_users(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "diogo",
                "email": "diogo@ufpb.com",
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        "/users/1",
        json={
            "username": "mateus",
            "email": "mateus@ufpb.com",
            "password": "mateus123",
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "mateus",
        "email": "mateus@ufpb.com",
    }


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "mateus",
        "email": "mateus@ufpb.com",
    }
