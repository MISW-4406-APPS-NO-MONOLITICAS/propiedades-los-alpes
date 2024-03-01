from uuid import uuid4
from flask.testing import FlaskClient
from pulsar import logging
from listados.modulos.contratos.aplicacion.comandos.crear_transaccion import (
    CrearTransaccion,
)
from listados.modulos.contratos.aplicacion.handlers import (
    TransaccionCreadaIntegracionHandler,
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
    # Termina los procesos que están escuchando los eventos de pulsar (broker)
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
    data.comprador = str(uuid4())
    with caplog.at_level(logging.INFO):
        response = client.post("/contratos", json=data.as_dict())
        assert response.status_code == 202
        name, topico = (
            TransaccionCreadaIntegracion.__name__,
            TransaccionCreadaIntegracion.topic_name(),
        )
        assert f"Evento {name} publicado en el topico {topico}" in caplog.text

    repositorio = RepositorioTrasaccionesDB()
    result = repositorio.obtener_por_columna("comprador", data.comprador)[0]

    evento = TransaccionCreadaIntegracion(
        id=str(uuid4()),
        fecha_evento=result.fecha_creacion.isoformat(),
        id_transaccion=result.id.__str__(),
        valor=result.valor.valor,
        fecha_creacion=result.fecha_creacion.isoformat(),
    )
    TransaccionCreadaIntegracionHandler(evento)
