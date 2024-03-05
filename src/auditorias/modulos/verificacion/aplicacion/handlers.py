import datetime
import random
import uuid
from auditorias.modulos.verificacion.aplicacion.comandos.auditar_contrato import ComandoAuditarContrato
from auditorias.modulos.verificacion.dominio.eventos import ContratoCreadoIntegracion
from auditorias.modulos.verificacion.aplicacion.mapeadores import MapeadorAnalisisDTOJson
from auditorias.config.logger import logger
from auditorias.modulos.verificacion.dominio.servicios import ServicioAuditoria
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando


class ContratoCreadoIntegracionHandler:
    servicio_auditoria: ServicioAuditoria = ServicioAuditoria()
    
    def __init__(self, event: ContratoCreadoIntegracion):
        logger.info(
            f"Handling evento {type(event).__name__}, id_transaccion: {event.id_transaccion}: {event}"
        )
        logger.info(
            f"EXPERIMENT - INICIAL: id_transaccion: {event.id_transaccion}, inicio-evento: {event.fecha_evento}, inicio-proceso: {datetime.datetime.now().isoformat()}"
        )
        analisis = self.servicio_auditoria.auditar_contrato(event)
        logger.info(f"analisis de contrato: {analisis}")
        
        if analisis.auditado:
            comando = ComandoAuditarContrato(
                tipo_analisis = analisis.tipo_analisis.valor,
                contrato_id = analisis.contrato_id,
                oficial = analisis.oficial,
                consistente = analisis.consistente,
                completo = analisis.completo,
                indice_confiabilidad = analisis.indice_confiabilidad,
                auditado = analisis.auditado,
            )
            ejecutar_comando(comando)
    
