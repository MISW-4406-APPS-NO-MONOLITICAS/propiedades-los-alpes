from listados.modulos.arrendamiento.dominio.repositorios import RepositorioArrendamiento
from listados.modulos.arrendamiento.infraestructura.repositorios import (
    RepositorioArrendamientoDB,
)
from listados.seedwork.aplicacion.comandos import ComandoHandler
from listados.modulos.arrendamiento.aplicacion.fabricas import FabricaArrendamientos


class BaseHandler(ComandoHandler):
    fabrica_arrendamientos: FabricaArrendamientos
    repositorio_arrendamientos: RepositorioArrendamiento

    def __init__(self):
        self.fabrica_arrendamientos: FabricaArrendamientos = FabricaArrendamientos()
        self.repositorio_arrendamientos: RepositorioArrendamiento = (
            RepositorioArrendamientoDB())
