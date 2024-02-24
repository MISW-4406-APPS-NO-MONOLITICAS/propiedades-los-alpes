from abc import ABC
from listados.seedwork.dominio.repositorios import Repositorio

class RepositorioReservas(Repositorio, ABC):
    ...

class RepositorioProveedores(Repositorio, ABC):
    ...