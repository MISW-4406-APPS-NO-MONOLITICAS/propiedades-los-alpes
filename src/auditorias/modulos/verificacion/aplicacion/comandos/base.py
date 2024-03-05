from auditorias.modulos.verificacion.dominio.repositorios import RepositorioAnalisis
from auditorias.modulos.verificacion.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from auditorias.seedwork.aplicacion.comandos import ComandoHandler
from auditorias.modulos.verificacion.aplicacion.fabricas import FabricaAnalisis


class BaseHandler(ComandoHandler):
    fabrica_transacciones: FabricaAnalisis
    repositorio_transaciones: RepositorioAnalisis

    def __init__(self):
        self.fabrica_transacciones: FabricaAnalisis = FabricaAnalisis()
        self.repositorio_transaciones: RepositorioAnalisis = (
            RepositorioTrasaccionesDB()
        )
