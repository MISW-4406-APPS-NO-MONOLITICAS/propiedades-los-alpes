from abc import ABC, abstractmethod
from typing import Type
from contratos.seedwork.aplicacion.comandos import Comando
from contratos.seedwork.dominio.eventos import EventoIntegracion
from dataclasses import dataclass, field
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
    dispatch_locally: bool = True


@dataclass
class CoordinadorSaga(ABC):
    id_correlacion: str
    index: int
    last_event_processed: str | None
    last_command_dispatched: str | None
    fecha_creacion: datetime.datetime
    fecha_actualizacion: datetime.datetime
    estado: str = "INICIADA"
    comandos_a_publicar: list[Comando] = field(default_factory=list)

    @staticmethod
    @abstractmethod
    def pasos() -> list[Paso]:
        ...

    def length(self):
        return len(self.pasos())

    def agregar_comando(self, comando: Comando):
        self.last_command_dispatched = comando.__class__.__name__
        self.comandos_a_publicar.append(comando)

    def publicar_comandos(self):
        for comando in self.comandos_a_publicar:
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
