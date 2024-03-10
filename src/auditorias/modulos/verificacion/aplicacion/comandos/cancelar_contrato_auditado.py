from uuid import uuid4
from auditorias.config.logger import logger
from auditorias.modulos.verificacion.dominio.servicios import ServicioAuditoria
from .base import BaseHandler
from auditorias.seedwork.aplicacion.comandos import Comando
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando as comando
from auditorias.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from auditorias.modulos.verificacion.aplicacion.dto import CompensacionDTO
import pulsar.schema as schema


class ComandoCancelarContratoAuditado(Comando):
    fecha_evento = schema.String(required=True)
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_auditoria = schema.String(required=True)

    def topic_name(self):
        return "auditorias_cancelar_contrato_auditado"

    def as_dict(self):
        return {
            "fecha_evento": self.fecha_evento,
            "id_correlacion": self.id_correlacion,
            "id_transaccion": self.id_transaccion,
            "id_auditoria": self.id_auditoria
        }
   
    
class ComandoCancelarContratoAuditadoHandler(BaseHandler):
    servicio_auditoria: ServicioAuditoria = ServicioAuditoria()
  
    def handle(self, comando: ComandoCancelarContratoAuditado):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        transaccion_cancelar_dto = CompensacionDTO(
            fecha_evento = comando.fecha_evento, 
            id_correlacion = comando.id_correlacion,
            id_transaccion = comando.id_transaccion,
            id_auditoria = comando.id_auditoria
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
