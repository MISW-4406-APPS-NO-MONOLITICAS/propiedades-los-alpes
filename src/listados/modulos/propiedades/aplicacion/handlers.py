import random
import uuid
from listados.modulos.propiedades.dominio.eventos import  PropiedadCreadaIntegracion
from listados.config.logger import logger
from listados.seedwork.aplicacion.handlers import Handler
from listados.modulos.propiedades.infraestructura.repositorios import (
    RepositorioPropiedadesDB,
)
from listados.modulos.propiedades.aplicacion.comandos.crear_propiedad import (
    ComandoCrearPropiedad,
)
from pydispatch import dispatcher



class HandlerArrendamientoDominio(Handler):
    @staticmethod
    def handle_arrendamiento_realizado(evento):
        logger.info(f"Handling evento de dominio {type(evento).__name__}")
        
def registrar():
    dispatcher.connect(
        HandlerArrendamientoDominio.handle_arrendamiento_realizado,
        signal="ArrendamientoRealizadoDominio",
    )       


class PropiedadCreadaIntegracionHandler:
    def __init__(self, event: PropiedadCreadaIntegracion):
        logger.info(
            f"Handling evento {type(event).__name__}, id_propiedad: {event.id_propiedad}"
        )

        repository = RepositorioPropiedadesDB()
        id_transaccion = uuid.UUID(str(event.id_propiedad))
        found = repository.obtener_por_id(id_transaccion)
        if found:
            logger.info(
                f"Transaccion {event.id_propiedad} ya existe, no se hace nada"
            )

            # Test
            if random.choice([True, False]):
                example_enviar_comando()

        else:
            logger.info(f"Transaccion {event.id_propiedad} no existe, se crea")


def example_enviar_comando():
    from faker import Faker
    faker = Faker()
    comando = ComandoCrearPropiedad(
        tipo_construccion=faker.word(),
        estado=faker.boolean(),
        area=faker.pyfloat(),
        direccion=faker.address(),
        lote=faker.random_int(min=1, max=100),
        compania=faker.company(),
        fecha_registro=faker.date_this_year(),
        fecha_actualizacion=faker.date_this_year(),
    )
    dispatcher.send(signal="Comando", comando=comando)
