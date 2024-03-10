"""Entidades reusables parte del seedwork del proyecto
"""

from dataclasses import dataclass, field
from datetime import datetime
import uuid
import pulsar.schema as schema
from pydispatch import dispatcher
from contratos.config.logger import logger


@dataclass
class EventoDominio:
    id: uuid.UUID = field(hash=True, default_factory=uuid.uuid4)
    fecha_evento: datetime = field(default_factory=datetime.now)


class EventoIntegracion(schema.Record):
    id_correlacion = schema.String()

    def topic_name(self) -> str:
        raise ValueError("La subclase debe implementar el método topic_name")


def despachar_evento_integracion(evento: EventoIntegracion):
    dispatcher.send(signal="Integracion", evento=evento)


def despachar_evento_integracion_localmente(evento: EventoIntegracion):
    logger.getChild("despachador-eventos").info(
        f"Despachando evento {evento.__class__.__name__} localmente"
    )
    dispatcher.send(signal=evento.__class__.__name__, evento=evento)
