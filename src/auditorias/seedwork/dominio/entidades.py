import uuid
from datetime import datetime
from dataclasses import dataclass, field

from auditorias.seedwork.infraestructura.eventos import EventoIntegracion
from .eventos import EventoDominio
from .mixins import ValidarReglasMixin

@dataclass
class Entidad:
    id: uuid.UUID = field(hash=True, default_factory=uuid.uuid4)
    fecha_creacion: datetime = field(default_factory=datetime.now)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)


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
