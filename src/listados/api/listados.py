import json
from flask import Blueprint, request, Response
from listados.modulos.propiedades.aplicacion.queries.obtener_listado_contratos import (
    ObtenerTransacciones,
)
from listados.seedwork.aplicacion.queries import ejecutar_query
from listados.modulos.propiedades.aplicacion.mapeadores import MapeadorPropiedadDTOJson
from listados.modulos.propiedades.aplicacion.comandos.crear_transaccion import (
    ComandoCrearTransaccion,
)
from contratos.seedwork.aplicacion.comandos import ejecutar_commando
from contratos.seedwork.dominio.excepciones import ExcepcionDominio

blueprint = Blueprint('contratos', __name__, url_prefix='/contratos')
mapeador = MapeadorPropiedadDTOJson()


@blueprint.route("", methods=("POST",))
def crear_propiedad():
    try:
        propiedad_dict = request.json

        transaccion_dto = mapeador.externo_a_dto(propiedad_dict)

        comando = ComandoCrearTransaccion(
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


@blueprint.route("", methods=("GET",))
def listar_transacciones():
    result = ejecutar_query(ObtenerTransacciones())
    return [mapeador.dto_a_externo(dto) for dto in result.resultado]
