""" from auditorias.modulos.verificacion.dominio.repositorios import RepositorioTransacciones
from auditorias.modulos.verificacion.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from auditorias.seedwork.aplicacion.comandos import ComandoHandler
from auditorias.modulos.verificacion.aplicacion.fabricas import FabricaTransacciones


class BaseHandler(ComandoHandler):
    fabrica_transacciones: FabricaTransacciones
    repositorio_transaciones: RepositorioTransacciones

    def __init__(self):
        self.fabrica_transacciones: FabricaTransacciones = FabricaTransacciones()
        self.repositorio_transaciones: RepositorioTransacciones = (
            RepositorioTrasaccionesDB()
        )
 """