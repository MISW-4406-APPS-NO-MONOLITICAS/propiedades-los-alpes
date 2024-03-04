import random
import uuid
from auditorias.modulos.verificacion.dominio.eventos import ContratoCreadoIntegracion
from auditorias.config.logger import logger
""" from auditorias.modulos.verificacion.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
) """
""" from auditorias.modulos.verificacion.aplicacion.comandos.modificar_contrato import (
    ComandoCrearTransaccion,
)
from pydispatch import dispatcher """


class ContratoCreadoIntegracionHandler:
    def __init__(self, event: ContratoCreadoIntegracion):
        logger.info(
            f"Handling evento {type(event).__name__}, id_transaccion: {event.id_transaccion}"
        )

""" def example_enviar_comando():
    from faker import Faker
    faker = Faker()
    comando = ComandoCrearTransaccion(
        valor=faker.random_number(),
        comprador=faker.name(),
        vendedor=faker.name(),
        inquilino=faker.name(),
        arrendatario=faker.name(),
    )
    dispatcher.send(signal="Comando", comando=comando) """
