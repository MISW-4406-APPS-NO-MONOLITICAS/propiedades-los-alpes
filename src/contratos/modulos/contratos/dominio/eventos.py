from __future__ import annotations
from dataclasses import dataclass, field
import uuid

from contratos.seedwork.dominio.eventos import EventoDominio, EventoIntegracion
from datetime import datetime
import pulsar.schema as schema


@dataclass
class TransaccionCreada(EventoDominio):
    id_transaccion: uuid.UUID = field(default_factory=uuid.uuid4)
    valor: float = field(default_factory=float)
    fecha_creacion: datetime = field(default_factory=datetime.now)


class TransaccionCreadaIntegracion(EventoIntegracion):
    id = schema.String(required=True)
    fecha_evento = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String(required=True)
    vendedor = schema.String(required=True)
    inquilino = schema.String(required=True)

    def topic_name(self):
        return "transaccion_creada"
