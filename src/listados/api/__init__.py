import os

from flask import Flask
from pydispatch.saferef import sys

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers_eventos_dominio():
    from listados.modulos.propiedades.aplicacion.handlers import (
        registrar as handler_propiedades,
    )

    handler_propiedades()


def registrar_consumidores_broker():
    import threading
    from listados.modulos.contratos.infraestructura.consumidores import consumidores

    for consumidor in consumidores:
        threading.Thread(target=consumidor).start()


def setup_db(app):
    # Inicializa la DB
    from listados.config.db import init_db, db_session

    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()


def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    # Base de datosath.join(basedir, 'database.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.secret_key = "9d58f98f-3ae8-4149-a09f-3a8c2012e32c"
    app.config["SESSION_TYPE"] = "filesystem"

    setup_db(app)

    registrar_handlers_eventos_dominio()
    from listados.config.pulsar import comenzar_despachador_eventos_integracion

    comenzar_despachador_eventos_integracion()
    if "pytest" not in sys.modules:
        registrar_consumidores_broker()

    # Importar Blueprints
    from . import propiedades
    from . import companias
    from . import contratos
    from . import planos

    # Registro de Blueprints
    app.register_blueprint(propiedades.bp)
    app.register_blueprint(companias.bp)
    app.register_blueprint(contratos.bp)
    app.register_blueprint(planos.bp)

    @app.route("/health")
    def __health():
        return {"status": "ok"}

    return app
