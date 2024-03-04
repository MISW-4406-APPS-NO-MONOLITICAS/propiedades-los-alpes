from listados.modulos.propiedades.dominio.repositorios import RepositorioPropiedades
from listados.modulos.propiedades.infraestructura.repositorios import (
    RepositorioPropiedadesDB,
)
from listados.seedwork.aplicacion.comandos import ComandoHandler
from listados.modulos.propiedades.aplicacion.fabricas import FabricaPropiedades


class BaseHandler(ComandoHandler):
    fabrica_propiedades: FabricaPropiedades
    repositorio_propiedades: RepositorioPropiedades

    def __init__(self):
        self.fabrica_propiedades: FabricaPropiedades = FabricaPropiedades()
        self.repositorio_propiedades: RepositorioPropiedades = (
            RepositorioPropiedadesDB())
