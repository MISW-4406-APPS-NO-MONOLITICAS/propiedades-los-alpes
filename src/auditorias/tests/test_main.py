from datetime import datetime
from uuid import uuid4
from flask.testing import FlaskClient
from pulsar import logging

from auditorias.modulos.verificacion.aplicacion.comandos.auditar_contrato import ComandoAuditarContratoIntegracion
from auditorias.modulos.verificacion.dominio.eventos import ContratoAuditadoIntegracion, ContratoRechazadoIntegracion
from auditorias.modulos.verificacion.infraestructura.repositorios import RepositorioAnalisisDB
""" from auditorias.modulos.verificacion.aplicacion.comandos.modificar_contrato import (
    ComandoCrearTransaccion,
)
from auditorias.modulos.verificacion.aplicacion.handlers import (
    TransaccionCreadaIntegracionHandler,
)
from auditorias.modulos.verificacion.dominio.eventos import TransaccionCreadaIntegracion
from auditorias.modulos.verificacion.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
) """
import pytest
import faker
from auditorias.api import create_app


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


def crear_data_contrato(rechazo = False):
    uuid = str(uuid4())
    return ComandoAuditarContratoIntegracion(
            id = uuid,
            fecha_evento = datetime.now().isoformat(),
            id_transaccion = uuid,
            valor = 0 if rechazo else faker.random_number(),
            comprador = faker.name(),
            vendedor = faker.name(),
            inquilino = faker.name(),
    )


def test_auditar_contrato_exitoso(client: FlaskClient, caplog: pytest.LogCaptureFixture):
    data = crear_data_contrato(rechazo = False)
    
    with caplog.at_level(logging.INFO):
        response = client.post("/auditorias", json=data.as_dict())
        assert response.status_code == 202
        name, topico = (
            ContratoAuditadoIntegracion.__name__,
            ContratoAuditadoIntegracion().topic_name(),
        )
        assert f"Publicado {name} en el topico {topico}" in caplog.text
    
    repositorio = RepositorioAnalisisDB()
    result = repositorio.obtener_por_columna("contrato_id", f"{data.id_transaccion}")
    assert len(result)
    assert result[0].contrato_id == data.id_transaccion
    assert result[0].auditado == 1

    return data
  
def test_auditar_contrato_rechazo(client: FlaskClient, caplog: pytest.LogCaptureFixture):
    data = crear_data_contrato(rechazo = True)
    
    with caplog.at_level(logging.INFO):
        response = client.post("/auditorias", json=data.as_dict())
        assert response.status_code == 202
        name, topico = (
            ContratoRechazadoIntegracion.__name__,
            ContratoRechazadoIntegracion().topic_name(),
        )
        assert f"Publicado {name} en el topico {topico}" in caplog.text
    
    repositorio = RepositorioAnalisisDB()
    result = repositorio.obtener_por_columna("contrato_id", f"{data.id_transaccion}")
    assert len(result)
    assert result[0].contrato_id == data.id_transaccion
    assert result[0].auditado == 0

    return data


