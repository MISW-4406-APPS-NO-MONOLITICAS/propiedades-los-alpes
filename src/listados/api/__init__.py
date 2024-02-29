import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))


def registrar_handlers():
    import listados.modulos.propiedades.aplicacion


def importar_modelos_alchemy():
    import listados.modulos.contratos.infraestructura.dto


def comenzar_consumidor():
    import threading
    import listados.modulos.propiedades.infraestructura.consumidores


def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    # Base de datosath.join(basedir, 'database.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.secret_key = "9d58f98f-3ae8-4149-a09f-3a8c2012e32c"
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["TESTING"] = configuracion.get("TESTING")

    # Inicializa la DB
    from listados.config.db import init_db

    init_db(app)
    from listados.config.db import db

    registrar_handlers()

    with app.app_context():
        importar_modelos_alchemy()
        print("Creando tablas en la base de datos")
        db.create_all()

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

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag["info"]["version"] = "1.0"
        swag["info"]["title"] = "Proyecto los Alpes"
        return jsonify(swag)

    @app.route("/health-check")
    def health():
        return jsonify({"status": "up"})

    return app
