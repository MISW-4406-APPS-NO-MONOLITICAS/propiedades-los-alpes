from datetime import datetime
import json
from uuid import uuid4
from flask.testing import FlaskClient
from pulsar import logging

from auditorias.modulos.verificacion.aplicacion.comandos.auditar_contrato import ComandoAuditarContrato
from auditorias.modulos.verificacion.aplicacion.comandos.cancelar_contrato_auditado import ComandoCancelarContratoAuditado
from auditorias.modulos.verificacion.infraestructura.repositorios import RepositorioAnalisisDB
from auditorias.modulos.verificacion.infraestructura.schema.v1.eventos import ContratoAuditadoIntegracion, ContratoAuditoriaRechazadaIntegracion, ContratoAuditadoCanceladoIntegracion
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
    id_correlacion = str(uuid4())
    id_transaccion = str(uuid4())
    return ComandoAuditarContrato(
        fecha_evento = datetime.now().isoformat(),
        id_correlacion = id_correlacion,
        id_transaccion = id_transaccion,
        valor = 0 if rechazo else faker.random_number(),
        comprador = faker.name(),
        vendedor = faker.name(),
        inquilino = faker.name(),
        arrendatario = faker.name(),
    )
    
def crear_data_compensacion(id_correlacion = "", id_transaccion = ""):
    uuid = str(uuid4())
    return ComandoCancelarContratoAuditado(
        fecha_evento = datetime.now().isoformat(),
        id_correlacion = id_correlacion,
        id_transaccion = id_transaccion,
        id_auditoria = uuid
    )


def test_auditar_contrato_exitoso(client: FlaskClient, caplog: pytest.LogCaptureFixture):
    # generar datos de contrato sin rechazo
    data = crear_data_contrato(rechazo = False)
    # capturar publicación en tópico
    with caplog.at_level(logging.INFO):
        response = client.post("/auditorias", json=data.as_dict())
        assert response.status_code == 202
        name, topico = (
            ContratoAuditadoIntegracion.__name__,
            ContratoAuditadoIntegracion().topic_name(),
        )
        assert f"Publicado {name} en el topico {topico}" in caplog.text
    # confirmar almacenamiento
    repositorio = RepositorioAnalisisDB()
    result = repositorio.obtener_por_columna("id_transaccion", f"{data.id_transaccion}")
    assert len(result)
    assert result[0].id_transaccion == data.id_transaccion
    assert result[0].auditado == 1
    # confirmar retorno en api
    response = client.get(f"/auditorias/contrato/{data.id_transaccion}")
    analisis_json = json.loads(response.data)
    assert response.status_code == 200
    assert analisis_json[0]["id_transaccion"] == data.id_transaccion
    assert analisis_json[0]["auditado"] == 1

    return data
  
def test_auditar_contrato_rechazo(client: FlaskClient, caplog: pytest.LogCaptureFixture):
    # generar datos de contrato incompleto
    data = crear_data_contrato(rechazo = True)
    # capturar publicación en tópico
    with caplog.at_level(logging.INFO):
        response = client.post("/auditorias", json=data.as_dict())
        assert response.status_code == 202
        name, topico = (
            ContratoAuditoriaRechazadaIntegracion.__name__,
            ContratoAuditoriaRechazadaIntegracion().topic_name(),
        )
        assert f"Publicado {name} en el topico {topico}" in caplog.text
    # confirmar almacenamiento
    repositorio = RepositorioAnalisisDB()
    result = repositorio.obtener_por_columna("id_transaccion", f"{data.id_transaccion}")
    assert len(result)
    assert result[0].id_transaccion == data.id_transaccion
    assert result[0].auditado == 0
    # confirmar retorno en api
    response = client.get(f"/auditorias/contrato/{data.id_transaccion}")
    analisis_json = json.loads(response.data)
    assert response.status_code == 200
    assert analisis_json[0]["id_transaccion"] == data.id_transaccion
    assert analisis_json[0]["auditado"] == 0

    return data

def test_auditar_contrato_compensacion(client: FlaskClient, caplog: pytest.LogCaptureFixture):
    # generar datos de contrato sin rechazo
    data = crear_data_contrato(rechazo = False)
    # capturar publicación en tópico
    with caplog.at_level(logging.INFO):
        response = client.post("/auditorias", json=data.as_dict())
        assert response.status_code == 202
        name, topico = (
            ContratoAuditadoIntegracion.__name__,
            ContratoAuditadoIntegracion().topic_name(),
        )
        assert f"Publicado {name} en el topico {topico}" in caplog.text
    # confirmar almacenamiento
    repositorio = RepositorioAnalisisDB()
    result = repositorio.obtener_por_columna("id_transaccion", f"{data.id_transaccion}")
    assert len(result)
    assert result[0].id_transaccion == data.id_transaccion
    assert result[0].auditado == 1
    # generar datos de compensación
    data_compensacion = crear_data_compensacion(f"{data.id_correlacion}", f"{data.id_transaccion}")
    # capturar publicación de compensación en tópico
    with caplog.at_level(logging.INFO):
        response = client.post("/auditorias/compensacion", json=data_compensacion.as_dict())
        assert response.status_code == 202
        name, topico = (
            ContratoAuditadoCanceladoIntegracion.__name__,
            ContratoAuditadoCanceladoIntegracion().topic_name(),
        )
        assert f"Publicado {name} en el topico {topico}" in caplog.text
    # confirmar retorno en api
    response = client.get(f"/auditorias/contrato/{data.id_transaccion}")
    analisis_json = json.loads(response.data)
    assert response.status_code == 200
    assert len(analisis_json) == 2
    assert len([analisis for analisis in analisis_json if analisis["auditado"] == 1]) == 1
    assert len([analisis for analisis in analisis_json if analisis["auditado"] == 0]) == 1

    return data


