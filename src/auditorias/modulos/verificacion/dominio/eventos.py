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


@dataclass
class ContratoRechazado(EventoDominio):
    id_transaccion: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    
class ContratoRechazadoIntegracion(EventoIntegracion):
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
        return "contrato_rechazado"