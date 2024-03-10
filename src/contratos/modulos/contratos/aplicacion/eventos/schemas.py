from __future__ import annotations
import pulsar.schema as schema
from contratos.seedwork.dominio.entidades import EventoIntegracion


class TransaccionCreadaIntegracion(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String(required=False)
    vendedor = schema.String(required=True)
    inquilino = schema.String(required=True)
    intermediario = schema.String(default=None, required_default=True)
    fecha_evento = schema.String(required=True)

    def topic_name(self):
        return "contratos_transaccion_creada"


class ContratoAuditado(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_auditoria = schema.String(required=True)

    def topic_name(self) -> str:
        return "auditorias_contrato_auditado"


class ContratoAuditoriaRechazada(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_auditoria = schema.String(required=True)

    def topic_name(self) -> str:
        return "auditorias_contrato_auditoria_rechazada"


class PropiedadArrendada(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    id_transaccion = schema.String(required=True)

    def topic_name(self) -> str:
        return "listados_propiedad_arrendada"


class PropiedadArrendamientoRechazado(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    id_transaccion = schema.String(required=True)

    def topic_name(self) -> str:
        return "listados_arrendamiento_fallido"
