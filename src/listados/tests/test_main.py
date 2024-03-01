from flask.testing import FlaskClient
from pulsar import logging
from listados.modulos.contratos.aplicacion.comandos.crear_transaccion import (
    CrearTransaccion,
)
from listados.modulos.contratos.dominio.eventos import TransaccionCreadaIntegracion
from listados.modulos.contratos.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
import pytest
import faker
from listados.api import create_app


faker = faker.Faker()


@pytest.fixture
def app():
    app = create_app()
    yield app
    processes = app.config.get("processes")
    if processes:
        for process in processes:
            process.terminate()


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


def test_crear_transaccion_evento_integracion(
    client: FlaskClient, caplog: pytest.LogCaptureFixture
):
    data = crear_transaccion_data()
    with caplog.at_level(logging.INFO):
        response = client.post("/contratos", json=data.as_dict())
        assert response.status_code == 202
        name, topico = (
            TransaccionCreadaIntegracion.__name__,
            TransaccionCreadaIntegracion.topic_name(),
        )
        assert f"Evento {name} publicado en el topico {topico}" in caplog.text
