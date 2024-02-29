from dataclasses import asdict, dataclass
from functools import singledispatch
from abc import ABC, abstractmethod
from typing import Any, Type


@dataclass
class Comando:
    ...

    def as_dict(self):
        return asdict(self)


class ComandoHandler(ABC):
    @abstractmethod
    def handle(self, comando: Type[Comando]) -> Any:
        raise NotImplementedError()


@singledispatch
def ejecutar_commando(comando):
    raise NotImplementedError(
        f"No existe implementación para el comando de tipo {type(comando).__name__}"
    )
