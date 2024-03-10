import pulsar.schema as schema
from auditorias.seedwork.infraestructura.eventos import EventoIntegracion


class ContratoAuditadoIntegracion(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_auditoria = schema.String(required=True)
    
    def topic_name(self):
        return "auditorias_contrato_auditado"
      
      
class ContratoAuditoriaRechazadaIntegracion(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_auditoria = schema.String(required=True)
    
    def topic_name(self):
        return "auditorias_contrato_auditoria_rechazada"
      
      
class ContratoAuditadoCanceladoIntegracion(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_auditoria = schema.String(required=True)
    
    def topic_name(self):
        return "auditorias_contrato_auditado_cancelado"