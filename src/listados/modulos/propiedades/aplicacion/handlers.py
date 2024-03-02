import random
import uuid
from listados.modulos.propiedades.dominio.eventos import TransaccionCreadaIntegracion
from listados.config.logger import logger
from listados.modulos.propiedades.infraestructura.repositorios import (
    RepositorioTrasaccionesDB,
)
from listados.modulos.propiedades.aplicacion.comandos.crear_transaccion import (
    ComandoCrearTransaccion,
)
from pydispatch import dispatcher


class TransaccionCreadaIntegracionHandler:
    def __init__(self, event: TransaccionCreadaIntegracion):
        logger.info(
            f"Handling evento {type(event).__name__}, id_transaccion: {event.id_transaccion}"
        )

        repository = RepositorioTrasaccionesDB()
        id_transaccion = uuid.UUID(str(event.id_transaccion))
        found = repository.obtener_por_id(id_transaccion)
        if found:
            logger.info(
                f"Transaccion {event.id_transaccion} ya existe, no se hace nada"
            )

            # Test
            if random.choice([True, False]):
                example_enviar_comando()

        else:
            logger.info(f"Transaccion {event.id_transaccion} no existe, se crea")


def example_enviar_comando():
    from faker import Faker
    faker = Faker()
    comando = ComandoCrearTransaccion(
        valor=faker.random_number(),
        comprador=faker.name(),
        vendedor=faker.name(),
        inquilino=faker.name(),
        arrendatario=faker.name(),
    )
    dispatcher.send(signal="Comando", comando=comando)