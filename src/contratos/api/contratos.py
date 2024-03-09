import json
import uuid
from flask import Blueprint, request, Response
from contratos.modulos.contratos.aplicacion.comandos.crear_contrato import (
    ComandoCrearContrato,
)
from contratos.modulos.contratos.aplicacion.queries.obtener_listado_contratos import (
    ObtenerTransacciones,
)
from contratos.seedwork.aplicacion.queries import ejecutar_query
from contratos.modulos.contratos.aplicacion.mapeadores import MapeadorTransaccionDTOJson
from contratos.modulos.contratos.aplicacion.comandos.crear_transaccion import (
    ComandoCrearTransaccion,
)
from contratos.seedwork.aplicacion.comandos import ejecutar_commando, ejecutar_commando_async
from contratos.seedwork.dominio.excepciones import ExcepcionDominio

blueprint = Blueprint("contratos", __name__, url_prefix="/contratos")
mapeador = MapeadorTransaccionDTOJson()


@blueprint.route("", methods=("POST",))
def crear_contrato():
    comando = ComandoCrearContrato(id_correlacion=str(uuid.uuid4()))
    ejecutar_commando(comando)
    return Response("{}", status=202, mimetype="application/json")


@blueprint.route("/transaccion", methods=("POST",))
def crear_transaccion():
    try:
        transaccion_dict = request.json

        transaccion_dto = mapeador.externo_a_dto(transaccion_dict)

        comando = ComandoCrearTransaccion(
            id_correlacion=str(uuid.uuid4()),
            valor=transaccion_dto.valor.valor,
            comprador=transaccion_dto.comprador,
            vendedor=transaccion_dto.vendedor,
            inquilino=transaccion_dto.inquilino,
            arrendatario=transaccion_dto.arrendatario,
        )
        ejecutar_commando(comando)
        return Response("{}", status=202, mimetype="application/json")
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )


@blueprint.route("/transaccion", methods=("GET",))
def listar_transacciones():
    result = ejecutar_query(ObtenerTransacciones())
    return [mapeador.dto_a_externo(dto) for dto in result.resultado]
