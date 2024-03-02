from listados.modulos.propiedades.dominio.repositorios import RepositorioTransacciones
from listados.modulos.propiedades.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from listados.seedwork.aplicacion.comandos import ComandoHandler
from listados.modulos.propiedades.aplicacion.fabricas import FabricaTransacciones


class BaseHandler(ComandoHandler):
    fabrica_transacciones: FabricaTransacciones
    repositorio_transaciones: RepositorioTransacciones

    def __init__(self):
        self.fabrica_transacciones: FabricaTransacciones = FabricaTransacciones()
        self.repositorio_transaciones: RepositorioTransacciones = (
            RepositorioTrasaccionesDB())
