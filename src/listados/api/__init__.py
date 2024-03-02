import os

from flask import Flask
from pydispatch.saferef import sys
from listados.config.pulsar import (
    comenzar_despachador_eventos_integracion_a_pulsar,
    comenzar_despachador_coamndos_a_pulsar,
)

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers_eventos_dominio():
    from listados.modulos.arrendamiento.aplicacion.handlers import (
        registrar as handler_arrendamiento,
    )

    handler_arrendamiento()


def comenzar_procesos_consumidores_de_pulsar(app: Flask):
    processes = []
    import multiprocessing
    from listados.modulos.propiedades.infraestructura.consumidores import consumidores

    for consumidor in consumidores:
        # Cada uno es un proceso bloqueante que está escuchando un tópico
        process = multiprocessing.Process(target=consumidor)
        processes.append(process)
        process.start()

    app.config["processes"] = processes


def setup_db(app: Flask):
    # Inicializa la DB
    from listados.config.db import init_db, db_session

    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()


def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = "9d58f98f-3ae8-4149-a09f-3a8c2012e32c"
    app.config["SESSION_TYPE"] = "filesystem"

    # Creación de las tablas y la sessión
    setup_db(app)

    # Handlers que escuchan eventos de dominio (síncronos)
    registrar_handlers_eventos_dominio()

    # Escucha los eventos de integración disparados por el uow, y los envía a los tópicos
    comenzar_despachador_eventos_integracion_a_pulsar()

    # Escucha los comandos disparados por la aplicación y los envía a los tópicos
    comenzar_despachador_coamndos_a_pulsar()

    # Cada consumidor tiene su propio proceso donde escucha un tópico con un esquema
    comenzar_procesos_consumidores_de_pulsar(app)

    # Importar Blueprints
    from . import listados

    # Registro de Blueprints
    app.register_blueprint(listados.blueprint)

    @app.route("/health")
    def __health():
        return {"status": "ok"}

    return app
