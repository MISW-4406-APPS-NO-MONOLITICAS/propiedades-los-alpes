from dataclasses import asdict, dataclass
from functools import singledispatch
from abc import ABC, abstractmethod
from typing import Any, Type
import pulsar.schema as schema


class Comando(schema.Record):
    def topic_name(self) -> str:
        raise ValueError("La subclase debe implementar el método topic_name")


class ComandoHandler(ABC):
    @abstractmethod
    def handle(self, comando: Type[Comando]) -> Any:
        raise NotImplementedError()


@singledispatch
def ejecutar_comando(comando):
    raise NotImplementedError(
        f"No existe implementación para el comando de tipo {type(comando).__name__}"
    )
