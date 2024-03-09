from __future__ import annotations
from dataclasses import asdict, dataclass
from functools import singledispatch
from pydispatch import dispatcher
from abc import ABC, abstractmethod
from typing import Any, Type
import pulsar.schema as schema

from contratos.seedwork.dominio.eventos import EventoIntegracion
from contratos.seedwork.dominio.eventos import EventoDominio


class Comando(schema.Record):
    id_correlacion = schema.String(required=True)

    def topic_name(self) -> str:
        raise ValueError("La subclase debe implementar el método topic_name")

    @staticmethod
    def from_evento(evento: EventoIntegracion) -> Comando:
        raise ValueError("La subclase debe implementar el método from_evento")


class ComandoHandler(ABC):
    @abstractmethod
    def handle(self, comando: Type[Comando]) -> Any:
        raise NotImplementedError()


@singledispatch
def ejecutar_commando(comando):
    raise NotImplementedError(
        f"No existe implementación para el comando de tipo {type(comando).__name__}"
    )

def ejecutar_commando_async(comando):
    dispatcher.send(signal="Comando", comando=comando)
