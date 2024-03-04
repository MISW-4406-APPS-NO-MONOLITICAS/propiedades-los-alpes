import random
from pydispatch import dispatcher
from listados.seedwork.aplicacion.handlers import Handler
from listados.modulos.arrendamiento.dominio.eventos import  ContratoPropiedadArrendadaIntegracion
from listados.config.logger import logger

logger = logger.getChild("arrendamiento-handler")


class ContratoPropiedadArrendadaIntegracionHandler:
    def __init__(self, event: ContratoPropiedadArrendadaIntegracion):
        logger.info(
            f"Handling evento {type(event).__name__}, id_propiedad: {event.id_propiedad}"
        )


# def example_enviar_comando():
#     from faker import Faker
#     faker = Faker()
#     comando = ComandoCrearPropiedad(
#         tipo_construccion=faker.word(),
#         estado=faker.boolean(),
#         area=faker.pyfloat(),
#         direccion=faker.address(),
#         lote=faker.random_int(min=1, max=100),
#         compania=faker.company(),
#         fecha_registro=faker.date_this_year(),
#         fecha_actualizacion=faker.date_this_year(),
#     )
#     dispatcher.send(signal="Comando", comando=comando)
