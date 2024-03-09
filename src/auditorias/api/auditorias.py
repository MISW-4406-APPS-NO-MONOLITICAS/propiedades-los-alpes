from datetime import datetime
import json
from uuid import uuid4
from auditorias.config.logger import logger
from auditorias.modulos.verificacion.aplicacion.comandos.auditar_contrato import ComandoAuditarContrato, ComandoAuditarContratoIntegracion
from auditorias.modulos.verificacion.aplicacion.comandos.eliminar_analisis import ComandoEliminarAnalisis
from flask import Blueprint, request, Response
from auditorias.modulos.verificacion.aplicacion.mapeadores import MapeadorTransaccionDTOJson
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando
from auditorias.seedwork.dominio.excepciones import ExcepcionDominio


blueprint = Blueprint('auditorias', __name__, url_prefix='/auditorias')
mapeador = MapeadorTransaccionDTOJson()

@blueprint.route("", methods=("POST",))
def probar_auditoria_contrato():
    try:
        transaccion_dict = request.json

        transaccion_dto = mapeador.externo_a_dto(transaccion_dict)
        #uuid = str(uuid4())

        comando = ComandoAuditarContratoIntegracion(
            id = transaccion_dto.id,
            fecha_evento = datetime.now().isoformat(),
            id_transaccion = transaccion_dto.contrato_id,
            valor = transaccion_dto.valor.valor,
            comprador = transaccion_dto.comprador,
            vendedor = transaccion_dto.vendedor,
            inquilino = transaccion_dto.inquilino,
        )
        ejecutar_comando(comando)
        return Response("{}", status=202, mimetype="application/json")
    except ExcepcionDominio as e:
        return Response(
            json.dumps(dict(error=str(e))), status=400, mimetype="application/json"
        )