from auditorias.config.logger import logger
from auditorias.modulos.verificacion.infraestructura.repositorios import RepositorioTrasaccionesDB
from auditorias.seedwork.aplicacion.queries import QueryResultado
from .base import BaseHandler
from auditorias.seedwork.aplicacion.comandos import Comando
from auditorias.seedwork.aplicacion.comandos import ejecutar_comando as comando
from auditorias.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from auditorias.modulos.verificacion.aplicacion.dto import AnalisisDTO, TipoAnalisis
import pulsar.schema as schema


class ComandoEliminarAnalisis(Comando):

    def topic_name(self):
        return "eliminar_analisis"

    def as_dict(self):
        return {}


class ComandoEliminarAnalisisHandler(BaseHandler):
    def handle(self, comando: ComandoEliminarAnalisis):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        repositorio = RepositorioTrasaccionesDB()
        return QueryResultado(repositorio.eliminar_todo())


@comando.register(ComandoEliminarAnalisis)
def ejecutar_comando_auditar_contrato(comando: ComandoEliminarAnalisis):
    handler = ComandoEliminarAnalisisHandler()
    handler.handle(comando)
