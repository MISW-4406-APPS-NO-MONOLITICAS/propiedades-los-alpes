"""Entidades reusables parte del seedwork del proyecto
"""

from dataclasses import dataclass, field
from datetime import datetime
import uuid
import pulsar.schema as schema


@dataclass
class EventoDominio:
    id: uuid.UUID = field(hash=True, default_factory=uuid.uuid4)
    fecha_evento: datetime = field(default=datetime.now())

class EventoIntegracion(schema.Record):
    def topic_name(self) -> str:
        raise ValueError("La subclase debe implementar el método topic_name")
