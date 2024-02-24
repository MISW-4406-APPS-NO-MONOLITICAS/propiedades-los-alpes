import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))

def registrar_handlers():
    import listados.modulos.contratos.aplicacion

def importar_modelos_alchemy():
    import listados.modulos.contratos.infraestructura.dto

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    # Base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa la DB
    from listados.config.db import init_db
    init_db(app)

    from listados.config.db import db

    importar_modelos_alchemy()
    registrar_handlers()

    with app.app_context():
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
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Proyecto los Alpes"
        return jsonify(swag)

    @app.route("/health-check")
    def health():
        return jsonify({"status": "up"})

    return app