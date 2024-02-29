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


class EventoIntegracion:
    topico: str
    evento: schema.Record

    def __init__(self, topico: str, evento: schema.Record):
        self.topico = topico
        self.evento = evento


class TransaccionCreadaIntegracion(schema.Record):
    id_transaccion = schema.String()
    valor = schema.Float()
    fecha_creacion = schema.String()
