from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from listados.seedwork.dominio.eventos import EventoDominio
from datetime import datetime
import pulsar.schema as schema


@dataclass
class TransaccionCreada(EventoDominio):
    id_transaccion: uuid.UUID = field(default_factory=uuid.uuid4)
    valor: float = field(default_factory=float)
    fecha_creacion: datetime = field(default_factory=datetime.now)


class TransaccionCreadaIntegracion(schema.Record):
    id = schema.String(required=True)
    fecha_evento = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    valor = schema.Float(required=True)
