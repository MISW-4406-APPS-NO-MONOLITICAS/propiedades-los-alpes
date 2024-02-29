import uuid
from datetime import datetime
from dataclasses import dataclass, field
from .eventos import EventoDominio, EventoIntegracion
from .mixins import ValidarReglasMixin
from .reglas import IdEntidadEsInmutable
from .excepciones import IdDebeSerInmutableExcepcion


@dataclass
class Entidad:
    id: uuid.UUID = field(hash=True, default_factory=uuid.uuid4)
    fecha_creacion: datetime = field(default=datetime.now())
    fecha_actualizacion: datetime = field(default=datetime.now())


@dataclass
class AgregacionRaiz(Entidad, ValidarReglasMixin):
    eventos: list[EventoDominio] = field(default_factory=list)
    eventos_integracion: list[EventoIntegracion] = field(default_factory=list)

    def agregar_evento(self, evento: EventoDominio):
        self.eventos.append(evento)

    def agregar_evento_integracion(self, evento: EventoIntegracion):
        self.eventos_integracion.append(evento)

    def limpiar_eventos(self):
        self.eventos = list()
