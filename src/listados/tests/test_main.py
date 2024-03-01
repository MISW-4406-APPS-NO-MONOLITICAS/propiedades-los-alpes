from flask.testing import FlaskClient
from sqlalchemy import text
from sqlalchemy.orm import Session
from listados.modulos.contratos.aplicacion.comandos.crear_transaccion import (
    CrearTransaccion,
)
from listados.modulos.contratos.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
import pytest
import faker
from listados.api import create_app
from listados.config.db import db_session


faker = faker.Faker()


@pytest.fixture
def app():
    app = create_app()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


def crear_transaccion_data():
    return CrearTransaccion(
        valor=faker.random_number(),
        comprador=faker.name(),
        vendedor=faker.name(),
        inquilino=faker.name(),
        arrendatario=faker.name(),
    )


def test_crear_transaccion(client: FlaskClient):
    data = crear_transaccion_data()
    response = client.post("/contratos", json=data.as_dict())
    assert response.status_code == 202

    repositorio = RepositorioTrasaccionesDB()
    result = repositorio.obtener_por_columna("comprador", data.comprador)
    assert len(result)
    assert result[0].comprador == data.comprador
    return data


def test_query_transacciones(client: FlaskClient):
    test_crear_transaccion(client)
    response = client.get("/contratos")
    assert response.status_code == 200
    # Assert is json
    assert response.is_json
    assert response.json
    for item in response.json:
        assert "valor" in item
        assert "comprador" in item
        assert "vendedor" in item
        assert "inquilino" in item
        assert "arrendatario" in item
