from http import HTTPStatus

from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_ok_e_ola_mundo():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Olá Mundo!"}


def test_html_deve_retornar_o_texto_da_pagina():
    client = TestClient(app)

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
