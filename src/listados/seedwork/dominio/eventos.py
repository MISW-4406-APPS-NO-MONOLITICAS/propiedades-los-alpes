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


# Este es el objeto que usamos para pasarle al despachador,
# simplemente tiene un tópico y el evento
@dataclass
class EventoIntegracion:
    topico: str
    evento: schema.Record
