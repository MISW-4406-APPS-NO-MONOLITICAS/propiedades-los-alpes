from contratos.modulos.contratos.dominio.repositorios import RepositorioTransacciones
from contratos.modulos.contratos.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from contratos.seedwork.aplicacion.comandos import ComandoHandler
from contratos.modulos.contratos.aplicacion.fabricas import FabricaTransacciones


class BaseHandler(ComandoHandler):
    fabrica_transacciones: FabricaTransacciones
    repositorio_transaciones: RepositorioTransacciones

    def __init__(self):
        self.fabrica_transacciones: FabricaTransacciones = FabricaTransacciones()
        self.repositorio_transaciones: RepositorioTransacciones = (
            RepositorioTrasaccionesDB()
        )
