import logging
from typing import Callable
import pulsar
import pulsar.schema as schema
from pydispatch import dispatcher
from listados.config.logger import logger

logger = logging.getLogger("pulsar")


def get_pulsar_client() -> pulsar.Client:
    logger = logging.getLogger("pulsar_client")
    logger.setLevel(logging.ERROR)
    return pulsar.Client(f"pulsar://pulsar:6650", logger=logger)


class Despachador:
    def _publicar_mensaje(self, topico: str, evento: schema.Record):
        cliente = get_pulsar_client()
        logger.info(f"Publicando evento {type(evento).__name__} en el topico {topico}")
        publicador = cliente.create_producer(
            topico, schema=schema.AvroSchema(evento.__class__)  # pyright: ignore
        )
        publicador.send(evento)
        logger.info(f"Evento {type(evento).__name__} publicado en el topico {topico}")
        cliente.close()

    def publicar_evento(self, evento):
        self._publicar_mensaje(evento.topico, evento.evento)


despachador = Despachador()


def comenzar_despachador_eventos_integracion():
    dispatcher.connect(despachador.publicar_evento, signal="Integracion")


class Consumidor:
    mensaje: schema.Record
    topico: str
    handler: Callable

    def __init__(self, topico: str, mensaje: schema.Record, handler: Callable):
        self.topico = topico
        self.mensaje = mensaje
        self.handler = handler

    def start(self):
        logger.info(f"Comenzando a consumir del topico {self.topico}")
        cliente = get_pulsar_client()
        consumidor = cliente.subscribe(
            self.topico,
            consumer_type=pulsar.ConsumerType.Shared,
            subscription_name="sub",
            schema=schema.AvroSchema(self.mensaje),  # pyright: ignore
        )
        while True:
            res = consumidor.receive()
            logger.info(f"Recibido mensaje del topico {self.topico}")
            value = res.value()
            logger.info(
                f"Mensaje deserializado de tipo {value.__class__.__name__} del topico {self.topico}"
            )
            self.handler(value)
            consumidor.acknowledge(res)
            logger.info(
                f"Acknowledged mensaje {value.__class__.__name__} del topico {self.topico}"
            )
