from auditorias.config.logger import logger
from auditorias.modulos.verificacion.dominio.objetos_valor import Valor
from auditorias.modulos.verificacion.dominio.servicios import ServicioAuditoria
from .base import BaseHandler
from auditorias.seedwork.aplicacion.comandos import Comando
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando as comando
from auditorias.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from auditorias.modulos.verificacion.aplicacion.dto import TransaccionDTO
import pulsar.schema as schema


class ComandoAuditarContrato(Comando):
    fecha_evento =  schema.String(required=True)
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String()
    vendedor = schema.String()
    inquilino = schema.String()        
    arrendatario = schema.String()        

    def topic_name(self):
        return "auditorias_auditar_contrato"

    def as_dict(self):
        return {
            "fecha_evento": self.fecha_evento,
            "id_correlacion": self.id_correlacion,
            "id_transaccion": self.id_transaccion,
            "valor": self.valor,
            "comprador": self.comprador,
            "vendedor": self.vendedor, 
            "inquilino": self.inquilino,
            "arrendatario": self.arrendatario
        }
        
    
class ComandoAuditarContratoHandler(BaseHandler):
    servicio_auditoria: ServicioAuditoria = ServicioAuditoria()
  
    def handle(self, comando: ComandoAuditarContrato):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        transaccion_dto = TransaccionDTO(
            fecha_evento = comando.fecha_evento,
            id_correlacion = comando.id_correlacion,
            id_transaccion = comando.id_transaccion,
            valor = Valor(comando.valor),
            comprador = comando.comprador,
            vendedor = comando.vendedor,
            inquilino = comando.inquilino,
            arrendatario = comando.arrendatario,
        )           
        
        analisis = self.servicio_auditoria.auditar_contrato(transaccion_dto)
        
        if analisis.auditado:
            analisis.guardar_analisis()  
        else:
            analisis.rechazar_contrato()
            
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
