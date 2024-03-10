from datetime import datetime
import json
from auditorias.modulos.verificacion.aplicacion.comandos.auditar_contrato import ComandoAuditarContrato
from flask import Blueprint, request, Response
from auditorias.modulos.verificacion.aplicacion.comandos.cancelar_contrato_auditado import ComandoCancelarContratoAuditado
from auditorias.modulos.verificacion.aplicacion.mapeadores import MapeadorAnalisisDTOJson, MapeadorCompensacionDTOJson, MapeadorTransaccionDTOJson
from auditorias.modulos.verificacion.aplicacion.queries.obtener_auditorias_contrato import ObtenerAuditoriasContrato
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando
from auditorias.seedwork.aplicacion.queries import ejecutar_query
from auditorias.seedwork.dominio.excepciones import ExcepcionDominio


blueprint = Blueprint('auditorias', __name__, url_prefix='/auditorias')
mapeador_transaccion = MapeadorTransaccionDTOJson()
mapeador_compensacion = MapeadorCompensacionDTOJson()

@blueprint.route("", methods=("POST",))
def probar_auditoria_contrato():
    try:
        transaccion_dict = request.json

        transaccion_dto = mapeador_transaccion.externo_a_dto(transaccion_dict)

        comando = ComandoAuditarContrato(
            fecha_evento = datetime.now().isoformat(),
            id_correlacion = transaccion_dto.id_correlacion,
            id_transaccion = transaccion_dto.id_transaccion,
            valor = transaccion_dto.valor.valor,
            comprador = transaccion_dto.comprador,
            vendedor = transaccion_dto.vendedor,
            inquilino = transaccion_dto.inquilino,
            arrendatario = transaccion_dto.arrendatario,
        )
        ejecutar_comando(comando)
        return Response("{}", status=202, mimetype="application/json")
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )
        
@blueprint.route("compensacion", methods=("POST",))
def probar_compensacion_contrato():
    try:
        compensacion_dict = request.json

        compensacion_dto = mapeador_compensacion.externo_a_dto(compensacion_dict)

        comando = ComandoCancelarContratoAuditado(
            fecha_evento = datetime.now().isoformat(),
            id_correlacion = compensacion_dto.id_correlacion,
            id_transaccion = compensacion_dto.id_transaccion,
            id_auditoria = compensacion_dto.id_auditoria
        )
        ejecutar_comando(comando)
        return Response("{}", status=202, mimetype="application/json")
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )
        
@blueprint.route("contrato/<id>", methods=("GET",))
def obtener_auditorias_por_contrato(id: str):
    result = ejecutar_query(ObtenerAuditoriasContrato(id_transaccion = id))
    map_auditoria = MapeadorAnalisisDTOJson()
    return [map_auditoria.dto_a_externo(analisis) for analisis in result.resultado]
