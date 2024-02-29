import json
from flask import request, Response
from listados.modulos.contratos.aplicacion.queries.obtener_listado_contratos import (
    ObtenerTransacciones,
)
from listados.seedwork.aplicacion.queries import ejecutar_query
import listados.seedwork.presentacion.api as api
from listados.modulos.contratos.aplicacion.mapeadores import MapeadorTransaccionDTOJson
from listados.modulos.contratos.aplicacion.comandos.crear_transaccion import (
    CrearTransaccion,
)
from listados.seedwork.aplicacion.comandos import ejecutar_commando
from listados.seedwork.dominio.excepciones import ExcepcionDominio

bp = api.crear_blueprint("contratos", "/contratos")


@bp.route("", methods=("POST",))
def crear_transaccion():
    try:
        transaccion_dict = request.json

        map_transaccion = MapeadorTransaccionDTOJson()
        transaccion_dto = map_transaccion.externo_a_dto(transaccion_dict)

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


@bp.route("", methods=("GET",))
def listar_transacciones():
    result = ejecutar_query(ObtenerTransacciones())
    return [MapeadorTransaccionDTOJson().dto_a_externo(dto) for dto in result.resultado]
