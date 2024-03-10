from __future__ import annotations
import pulsar.schema as schema
from contratos.seedwork.dominio.entidades import EventoIntegracion


class TransaccionCreadaIntegracionV1(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String(required=True)
    vendedor = schema.String(required=True)
    inquilino = schema.String(required=True)
    intermediario = schema.String(default=None, required_default=True)
    fecha_evento = schema.String(required=True)

    def topic_name(self):
        return "contratos_transaccion_creada"

    @staticmethod
    def from_v2(evento: TransaccionCreadaIntegracionV2):
        return TransaccionCreadaIntegracionV1(
            id_correlacion=evento.id_correlacion,
            id_transaccion=evento.id_transaccion,
            valor=evento.valor,
            comprador=evento.comprador if evento.comprador else 'SIN_COMPRADOR',
            vendedor=evento.vendedor,
            inquilino=evento.inquilino,
            intermediario=evento.intermediario,
            fecha_evento=evento.fecha_evento,
        )


class TransaccionCreadaIntegracionV2(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String(required=False)
    vendedor = schema.String(required=True)
    inquilino = schema.String(required=True)
    intermediario = schema.String(default=None, required_default=True)
    fecha_evento = schema.String(required=True)

    def topic_name(self):
        return "contratos_transaccion_creada_v2"


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
