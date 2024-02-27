import json
from flask import request, Response
import listados.seedwork.presentacion.api as api
from listados.modulos.contratos.aplicacion.mapeadores import MapeadorTransaccionDTOJson
from listados.modulos.contratos.aplicacion.comandos.crear_transaccion import CrearTransaccion
from listados.seedwork.aplicacion.comandos import ejecutar_commando
from listados.seedwork.dominio.excepciones import ExcepcionDominio

bp = api.crear_blueprint('contratos','/contratos')

@bp.route('',methods=('GET',))
@bp.route('/<id>',methods=('GET',))
def dar_contrato(id=None):
    if id:
        return {'message': f'Contrato {id} works !'}

    return {'message':'GET Contratos works !'}

@bp.route('',methods=('POST',))
def establecer_transaccion():
    try:
        transaccion_dict = request.json

        map_transaccion = MapeadorTransaccionDTOJson()
        transaccion_dto = map_transaccion.externo_a_dto(transaccion_dict)

        comando = CrearTransaccion(
            transaccion_dto.id,
            transaccion_dto.fecha_creacion,
            transaccion_dto.fecha_actualizacion,
            transaccion_dto.valor,
            transaccion_dto.comprador,
            transaccion_dto.vendedor,
            transaccion_dto.inquilino,
            transaccion_dto.arrendatario
        )
        ejecutar_commando(comando)
        return Response('{}', status=202, mimetype='application/json')
    except ExcepcionDominio as e:
        return Response(json.dumps(dict(error=str(e))), status=400, mimetype='application/json')