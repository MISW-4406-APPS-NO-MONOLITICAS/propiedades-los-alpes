""" Fábricas para la creación de objetos en la capa de infrastructura del dominio de contratos

"""

from dataclasses import dataclass, field
from listados.seedwork.dominio.fabricas import Fabrica
from listados.seedwork.dominio.repositorios import Repositorio
from listados.modulos.contratos.dominio.repositorios import RepositorioProveedores, RepositorioTransacciones
from .repositorios import RepositorioTrasaccionesDB, RepositorioProveedoresDB
from .excepciones import ExcepcionFabrica

@dataclass
class FabricaRepositorio(Fabrica):
    def crear_objeto(self, obj: type, mapeador: any = None) -> Repositorio:
        if obj == RepositorioTransacciones.__class__:
            return RepositorioTrasaccionesDB()
        elif obj == RepositorioProveedores.__class__:
            return RepositorioProveedoresDB()
        else:
            raise ExcepcionFabrica()