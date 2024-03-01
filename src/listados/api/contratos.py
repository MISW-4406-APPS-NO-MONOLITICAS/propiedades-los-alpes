import json
from flask import Blueprint, request, Response
from listados.modulos.contratos.aplicacion.queries.obtener_listado_contratos import (
    ObtenerTransacciones,
)
from listados.seedwork.aplicacion.queries import ejecutar_query
from listados.modulos.contratos.aplicacion.mapeadores import MapeadorTransaccionDTOJson
from listados.modulos.contratos.aplicacion.comandos.crear_transaccion import (
    CrearTransaccion,
)
from listados.seedwork.aplicacion.comandos import ejecutar_commando
from listados.seedwork.dominio.excepciones import ExcepcionDominio

blueprint = Blueprint('contratos', __name__, url_prefix='/contratos')
mapeador = MapeadorTransaccionDTOJson()


@blueprint.route("", methods=("POST",))
def crear_transaccion():
    try:
        transaccion_dict = request.json

        transaccion_dto = mapeador.externo_a_dto(transaccion_dict)

        comando = CrearTransaccion(
            transaccion_dto.valor,
            transaccion_dto.comprador,
            transaccion_dto.vendedor,
            transaccion_dto.inquilino,
            transaccion_dto.arrendatario,
        )
        ejecutar_commando(comando)
        return Response("{}", status=202, mimetype="application/json")
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )


@blueprint.route("", methods=("GET",))
def listar_transacciones():
    result = ejecutar_query(ObtenerTransacciones())
    return [mapeador.dto_a_externo(dto) for dto in result.resultado]
