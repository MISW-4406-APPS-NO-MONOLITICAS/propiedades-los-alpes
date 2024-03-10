from __future__ import annotations
from dataclasses import dataclass, field
import uuid

from auditorias.seedwork.dominio.eventos import EventoDominio, EventoIntegracion
from datetime import datetime
import pulsar.schema as schema


@dataclass
class ContratoAuditado(EventoDominio):
    id_transaccion: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_creacion: datetime = field(default_factory=datetime.now)


class ContratoAuditadoIntegracion(EventoIntegracion):
    id = schema.String(required=True)
    fecha_evento = schema.String(required=True)
    tipo_analisis = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    oficial = schema.Boolean(required=True)
    consistente = schema.Boolean(required=True)
    completo = schema.Boolean(required=True)
    indice_confiabilidad = schema.Float(required=True)
    auditado = schema.Boolean(required=True)

    def topic_name(self):
        return "contrato_auditado"


class ContratoCreadoIntegracion(EventoIntegracion):
    id = schema.String(required=True)
    fecha_evento = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String(required=True)
    vendedor = schema.String(required=True)
    inquilino = schema.String(required=True)

    def topic_name(self):
        return "transaccion_creada"


class TransaccionCreadaIntegracion(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String(required=True)
    vendedor = schema.String(required=True)
    inquilino = schema.String(required=True)
    fecha_evento = schema.String(required=True)

    def topic_name(self):
        return "contratos_transaccion_creada"
