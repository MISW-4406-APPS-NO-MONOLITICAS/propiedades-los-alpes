import uuid
from contratos.config.db import create_db_session
from contratos.modulos.contratos.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from contratos.seedwork.aplicacion.comandos import ComandoHandler
from contratos.config.logger import logger
from contratos.modulos.contratos.aplicacion.fabricas import FabricaTransacciones
from contratos.modulos.contratos.dominio.repositorios import RepositorioTransacciones
from contratos.seedwork.aplicacion.comandos import Comando
from contratos.seedwork.aplicacion.comandos import ejecutar_commando as comando
import pulsar.schema as schema


class ComandoCrearContrato(Comando):
    id_correlacion = schema.String(required=True)

    def topic_name(self) -> str:
        return "contrato_crear"


class ComandoAuditarContrato(Comando):
    id_correlacion = schema.String(required=True)

    def topic_name(self) -> str:
        return "auditoria_auditar"


class ComandoCrearContratoHandler(ComandoHandler):
    def __init__(self, db_session=None):
        self.fabrica_transacciones = FabricaTransacciones()
        self.repositorio_transaciones = RepositorioTrasaccionesDB(db_session=db_session)

    def handle(self, comando: ComandoCrearContrato):
        from contratos.modulos.sagas.saga import ManejadorDeSaga

        logger.info(
            f"Manejando comando %s con id_correlacion %s",
            comando.__class__.__name__,
            comando.id_correlacion,
        )
        comando_inicial = ComandoAuditarContrato(id_correlacion=comando.id_correlacion)
        ManejadorDeSaga().iniciar_saga(
            id_correlacion=comando.id_correlacion, comando_inicial=comando_inicial
        )


@comando.register(ComandoCrearContrato)
def ejecutar_comando_crear_transaccion(comando: ComandoCrearContrato):
    handler = ComandoCrearContratoHandler()
    handler.handle(comando)
