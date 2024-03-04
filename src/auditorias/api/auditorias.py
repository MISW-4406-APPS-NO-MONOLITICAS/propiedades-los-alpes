import json
from flask import Blueprint, request, Response
""" from auditorias.modulos.verificacion.aplicacion.queries.obtener_listado_auditorias import (
    ObtenerVerificaciones,
)
from auditorias.seedwork.aplicacion.queries import ejecutar_query
from auditorias.modulos.verificacion.aplicacion.mapeadores import MapeadorVerificacionDTOJson
from auditorias.modulos.verificacion.aplicacion.comandos.auditar_contrato import (
    ComandoEnriquecerContrato,
)
from auditorias.seedwork.aplicacion.comandos import ejecutar_commando
from auditorias.seedwork.dominio.excepciones import ExcepcionDominio """

blueprint = Blueprint('auditorias', __name__, url_prefix='/auditorias')
""" mapeador = MapeadorVerificacionDTOJson() """


""" @blueprint.route("", methods=("POST",))
def auditar_contrato():
    try:
        contrato_dict = request.json

        contrato_dto = mapeador.externo_a_dto(contrato_dict)

        comando = ComandoEnriquecerContrato(
            valor=contrato_dto.valor.valor,
            comprador=contrato_dto.comprador,
            vendedor=contrato_dto.vendedor,
            inquilino=contrato_dto.inquilino,
            arrendatario=contrato_dto.arrendatario,
        )
        ejecutar_commando(comando)
        return Response("{}", status=202, mimetype="application/json")
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )


@blueprint.route("", methods=("GET",))
def listar_transacciones():
    result = ejecutar_query(ObtenerVerificaciones())
    return [mapeador.dto_a_externo(dto) for dto in result.resultado] """
