from http import HTTPStatus

from fast_zero.schemas import UserPublic


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
            "username": "Teste",
            "email": "teste@teste.com",
            "password": "teste123",
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "id": 1,
        "username": "Teste",
        "email": "teste@teste.com",
    }


def test_create_user_with_an_existent_username(client, user):
    response = client.post(
        "/users",
        json={
            "username": "Teste",
            "email": "outroemail@teste.com",
            "password": "teste123",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_create_user_with_an_existent_email(client, user):
    response = client.post(
        "/users",
        json={
            "username": "OutroUser",
            "email": "teste@teste.com",
            "password": "teste123",
        },
    )
    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Email already exists"}


def test_read_users_with_no_users(client):
    response = client.get("/users")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get("/users")
    assert response.json() == {"users": [user_schema]}


def test_get_user_by_id(client, user):
    response = client.get(f"/users/{user.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "id": 1,
        "username": user.username,
        "email": user.email,
    }


def test_get_an_inexistent_user(client):
    response = client.get("/users/2")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_user(client, user):
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
        "id": 1,
        "username": "mateus",
        "email": "mateus@ufpb.com",
    }


def test_update_an_inexistent_user(client):
    response = client.put(
        "/users/2",
        json={
            "username": "aluno",
            "email": "aluno@ufpb.com",
            "password": "aluno123",
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_integrity_error(client, user):
    client.post(
        "/users",
        json={
            "username": "fausto",
            "email": "fausto@example.com",
            "password": "secret",
        },
    )

    response_update = client.put(
        f"/users/{user.id}",
        json={
            "username": "fausto",
            "email": "bob@example.com",
            "password": "secret",
        },
    )

    assert response_update.status_code == HTTPStatus.CONFLICT
    assert response_update.json() == {
        "detail": "Username or email already exists"
    }


def test_delete_user(client, user):
    response = client.delete(f"/users/{user.id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "User deleted"}


def test_delete_an_inexistent_user(client):
    response = client.delete("/users/2")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}
