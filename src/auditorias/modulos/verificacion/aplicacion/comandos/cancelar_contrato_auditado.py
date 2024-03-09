from dataclasses import dataclass, field
from uuid import uuid4
from auditorias.config.logger import logger
from auditorias.modulos.verificacion.dominio.objetos_valor import Valor
from auditorias.modulos.verificacion.dominio.servicios import ServicioAuditoria
from .base import BaseHandler
from auditorias.seedwork.aplicacion.comandos import Comando
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando as comando
from auditorias.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from auditorias.modulos.verificacion.aplicacion.dto import AnalisisDTO, TipoAnalisis, CompensacionDTO, TransaccionDTO
import pulsar.schema as schema


class ComandoCancelarContratoAuditado(Comando):
    id_transaccion = schema.String(required=True) 

    def topic_name(self):
        return "cancelar_contrato_auditado"

    def as_dict(self):
        return {
            "id_transaccion": self.id_transaccion,
        }


class ComandoCancelarContratoAuditadoIntegracion(ComandoCancelarContratoAuditado):
    id = schema.String(required=True)
    fecha_evento = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    
    
class ComandoCancelarContratoAuditadoHandler(BaseHandler):
    servicio_auditoria: ServicioAuditoria = ServicioAuditoria()
  
    def handle(self, comando: ComandoCancelarContratoAuditado):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        transaccion_cancelar_dto = CompensacionDTO(
            contrato_id = comando.id_transaccion
        )
        
        analisis = self.servicio_auditoria.buscar_analisis(transaccion_cancelar_dto)
        analisis.cancelar_contrato_auditado()
        #logger.info(f"analisis de contrato: {analisis}")
                    
        # Se programa en el uow
        logger.info(f"Inscribiendo en unidad de trabajo de {analisis.__class__.__name__}")
        analisis.id = uuid4()
        analisis.auditado = False
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_analisis.agregar, analisis
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(ComandoCancelarContratoAuditado)
def ejecutar_comando_auditar_contrato(comando: ComandoCancelarContratoAuditado):
    handler = ComandoCancelarContratoAuditadoHandler()
    handler.handle(comando)
