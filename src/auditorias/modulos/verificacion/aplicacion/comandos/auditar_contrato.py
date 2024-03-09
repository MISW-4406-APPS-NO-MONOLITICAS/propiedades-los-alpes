from dataclasses import dataclass, field
from auditorias.config.logger import logger
from auditorias.modulos.verificacion.dominio.objetos_valor import Valor
from auditorias.modulos.verificacion.dominio.servicios import ServicioAuditoria
from .base import BaseHandler
from auditorias.seedwork.aplicacion.comandos import Comando
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando as comando
from auditorias.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from auditorias.modulos.verificacion.aplicacion.dto import AnalisisDTO, TipoAnalisis, TransaccionDTO
import pulsar.schema as schema


class ComandoAuditarContrato(Comando):
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String(required=True)
    vendedor = schema.String(required=True)
    inquilino = schema.String(required=True)        

    def topic_name(self):
        return "auditar_contrato"

    def as_dict(self):
        return {
            # "id": self.id,
            # "fecha_evento": self.fecha_evento,
            "id_transaccion": self.id_transaccion,
            "valor": self.valor,
            "comprador": self.comprador,
            "vendedor": self.vendedor, 
            "inquilino": self.inquilino
        }


class ComandoAuditarContratoIntegracion(ComandoAuditarContrato):
    id = schema.String(required=True)
    fecha_evento = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String(required=True)
    vendedor = schema.String(required=True)
    inquilino = schema.String(required=True)  
    
    
class ComandoAuditarContratoHandler(BaseHandler):
    servicio_auditoria: ServicioAuditoria = ServicioAuditoria()
  
    def handle(self, comando: ComandoAuditarContrato):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        #logger.info(f"Contrato: {comando}")
        transaccion_dto = TransaccionDTO(
            contrato_id = comando.id_transaccion,
            valor = Valor(comando.valor),
            comprador = comando.comprador,
            vendedor = comando.vendedor,
            inquilino = comando.inquilino,
        )           
        
        analisis = self.servicio_auditoria.auditar_contrato(transaccion_dto)
        #logger.info(f"analisis de contrato: {analisis}")
        
        if analisis.auditado:
            analisis.guardar_analisis()  # Genera los eventos
        else:
            analisis.rechazar_contrato()
            
        # Se programa en el uow
        logger.info(f"Inscribiendo en unidad de trabajo de {analisis.__class__.__name__}")
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_analisis.agregar, analisis
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(ComandoAuditarContrato)
def ejecutar_comando_auditar_contrato(comando: ComandoAuditarContrato):
    handler = ComandoAuditarContratoHandler()
    handler.handle(comando)
