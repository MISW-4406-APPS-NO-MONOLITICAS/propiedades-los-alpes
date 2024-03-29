import os
import multiprocessing

from flask import Flask
from pydispatch.saferef import sys
from contratos.config.pulsar import Consumidor
from contratos.config.pulsar import (
    comenzar_despachador_eventos_integracion_a_pulsar,
    comenzar_despachador_coamndos_a_pulsar,
)

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers_eventos_dominio():
    from contratos.modulos.propiedades.aplicacion.handlers import (
        registrar as handler_propiedades,
    )
    from contratos.modulos.contratos.aplicacion.eventos.handlers import (
        registrar as handler_contratos,
    )

    handler_propiedades()
    handler_contratos()


def comenzar_procesos_consumidores_de_pulsar(app: Flask):
    processes = []
    todos: list[Consumidor] = []

    from contratos.modulos.contratos.infraestructura.consumidores import (
        consumidores as consumidores_contratos,
    )
    todos.extend(consumidores_contratos)

    from contratos.modulos.sagas.saga import consumidores as consumidores_sagas
    todos.extend(consumidores_sagas)

    # UNCOMMENT IF WE WANT TO MOCK THE SAGA COMMAND CONSUMERS
    # from contratos.modulos.sagas.consumidores import (
    #     consumidores as consumidores_sagas_helper,
    # )
    # todos.extend(consumidores_sagas_helper)

    for consumidor in todos:
        assert isinstance(consumidor, Consumidor)
        # Cada uno es un proceso bloqueante que está escuchando un tópico
        process = multiprocessing.Process(
            target=consumidor.start, name=consumidor.name()
        )
        processes.append(process)
        process.start()

    app.config["processes"] = processes


def setup_db(app: Flask):
    # Inicializa la DB
    from contratos.config.db import init_db, Session

    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        Session.remove()


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
    from . import contratos

    # Registro de Blueprints
    app.register_blueprint(contratos.blueprint)

    @app.route("/health")
    def __health():
        return {"status": "ok"}

    return app
