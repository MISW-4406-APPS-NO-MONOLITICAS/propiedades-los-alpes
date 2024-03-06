import json
from auditorias.modulos.verificacion.aplicacion.comandos.eliminar_analisis import ComandoEliminarAnalisis
from flask import Blueprint, request, Response
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando

blueprint = Blueprint('auditorias', __name__, url_prefix='/auditorias')
