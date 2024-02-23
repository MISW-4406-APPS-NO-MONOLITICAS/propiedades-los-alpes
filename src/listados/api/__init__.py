import os

from flask import Flask, render_template, request, url_for, redirect, jsonify, session
from flask_swagger import swagger

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app(configuracion={}):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

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