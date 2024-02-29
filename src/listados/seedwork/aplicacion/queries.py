from functools import singledispatch
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar


class Query(ABC):
    ...


T = TypeVar("T")


@dataclass
class QueryResultado(Generic[T]):
    resultado: T


class QueryHandler(ABC):
    @abstractmethod
    def handle(self, query: Query) -> QueryResultado:
        raise NotImplementedError()


@singledispatch
def ejecutar_query(query) -> QueryResultado:
    raise NotImplementedError(
        f"No existe implementación para el query de tipo {type(query).__name__}"
    )
