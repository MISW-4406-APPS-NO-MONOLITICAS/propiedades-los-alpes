#Interfaces para los repositorios reusables parte del seedwork del proyecto

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID
from .entidades import Entidad


class Repositorio(ABC):
    @abstractmethod
    def obtener_por_id(self, id: UUID) -> Entidad | None:
        ...

    def obtener_por_id_or_error(self, id: UUID) -> Entidad:
        result = self.obtener_por_id(id)
        if result is None:
            raise ValueError(f"No se encontró entidad con id {id}")
        return result

    @abstractmethod
    def obtener_todos(self) -> list[Entidad]:
        ...

    @abstractmethod
    def agregar(self, entity: Entidad):
        ...

    @abstractmethod
    def actualizar(self, entity: Entidad):
        ...

    @abstractmethod
    def eliminar(self, entity_id: UUID):
        ...


class Mapeador(ABC):
    @abstractmethod
    def entidad_a_dto(self, entidad: Any) -> Any:
        ...

    @abstractmethod
    def dto_a_entidad(self, dto: Any) -> Entidad:
        ...
