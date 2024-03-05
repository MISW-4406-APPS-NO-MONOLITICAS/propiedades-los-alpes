from abc import ABC
from listados.seedwork.dominio.repositorios import Repositorio


class RepositorioPropiedades(Repositorio, ABC):
    ...


class RepositorioArrendamiento(Repositorio, ABC):
    ...