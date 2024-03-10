from auditorias.modulos.verificacion.dominio.repositorios import RepositorioAnalisis
from auditorias.modulos.verificacion.infraestructura.repositorios import (
    RepositorioAnalisisDB,
)
from auditorias.seedwork.aplicacion.comandos import ComandoHandler
from auditorias.modulos.verificacion.aplicacion.fabricas import FabricaAnalisis


class BaseHandler(ComandoHandler):
    fabrica_analisis: FabricaAnalisis
    repositorio_analisis: RepositorioAnalisis

    def __init__(self):
        self.fabrica_analisis: FabricaAnalisis = FabricaAnalisis()
        self.repositorio_analisis: RepositorioAnalisis = (
            RepositorioAnalisisDB()
        )
