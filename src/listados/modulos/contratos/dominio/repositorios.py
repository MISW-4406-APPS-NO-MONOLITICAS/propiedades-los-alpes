from abc import ABC
from listados.seedwork.dominio.repositorios import Repositorio

class RepositorioTransacciones(Repositorio, ABC):
    ...

class RepositorioProveedores(Repositorio, ABC):
    ...