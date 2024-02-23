from flask import request, Response

import listados.seedwork.presentacion.api as api
from listados.modulos.propiedades.aplicacion.comandos.crear_propiedad import CrearPropiedad
#from propiedades_alpes.modulos.propiedades.aplicacion.queries import

bp = api.crear_blueprint('propiedades','/propiedades')

@bp.route('',methods=('GET',))
@bp.route('/<id>',methods=('GET',))
def dar_propiedade(id=None):
    if id:
        return {'message': f'Propiedad {id} works !'}

    return {'message':'GET Propiedades works !'}

@bp.route('',methods=('POST',))
def crear_propiedad():
    propiedad_dict = request.json

    return propiedad_dict