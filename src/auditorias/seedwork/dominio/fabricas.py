# Fábricas para la creación de objetos reusables parte del seedwork del proyecto

from abc import ABC, abstractmethod
from typing import Any
from .repositorios import Mapeador
from .mixins import ValidarReglasMixin


class Fabrica(ABC, ValidarReglasMixin):
    @abstractmethod
    def crear_objeto(self, obj, mapeador: Mapeador) -> Any:
        ...
