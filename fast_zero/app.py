from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from fast_zero.schemas import Message, UserSchema

app = FastAPI()


@app.get("/", status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {"message": "Olá Mundo!"}


@app.get("/html", response_class=HTMLResponse)
def exibir_html():
    return """
    <html>
        <head>
            <title> Nosso olá mundo </title>
         </head>
        <body>
            <h1>Algo diferente de olá mundo</h1>
        </body>
    </html>
    """


@app.post("/users", status_code=HTTPStatus.CREATED)
def create_user(user : UserSchema):
    return None
