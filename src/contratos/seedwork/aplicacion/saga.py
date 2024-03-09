from abc import ABC, abstractmethod
from typing import Type
from contratos.seedwork.aplicacion.comandos import Comando
from contratos.seedwork.dominio.eventos import EventoIntegracion
from dataclasses import dataclass
from pydispatch import dispatcher
import uuid
import datetime


@dataclass
class Paso:
    index: int
    comando: Type[Comando]
    evento: Type[EventoIntegracion]
    error: Type[EventoIntegracion]
    compensacion: Type[Comando] | None


@dataclass
class CoordinadorSaga(ABC):
    id_correlacion: str
    index: int
    last_event_processed: str | None
    last_command_dispatched: str | None
    fecha_creacion: datetime.datetime
    fecha_actualizacion: datetime.datetime
    estado: str = "INICIADA"

    @staticmethod
    @abstractmethod
    def pasos() -> list[Paso]:
        ...

    def length(self):
        return len(self.pasos())

    def publicar_comando(self, comando: Comando):
        self.last_command_dispatched = comando.__class__.__name__
        dispatcher.send(signal="Comando", comando=comando)

    @abstractmethod
    def procesar_evento(self, evento: EventoIntegracion) -> None:
        ...

    @abstractmethod
    def completada(self):
        self.estado = "COMPLETADA"

    def revertida(self):
        self.estado = "REVERTIDA"

    @staticmethod
    @abstractmethod
    def eventos_a_escuchar() -> list[type[EventoIntegracion]]:
        ...
