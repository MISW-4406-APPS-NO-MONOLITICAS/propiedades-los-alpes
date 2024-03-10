import logging
from typing import Callable
import pulsar
import pulsar.schema as schema
from pydispatch import dispatcher
from contratos.config.logger import logger
from contratos.seedwork.aplicacion.comandos import Comando
from contratos.seedwork.dominio.eventos import EventoIntegracion

logger = logging.getLogger("pulsar")


def get_pulsar_client() -> pulsar.Client:
    logger = logging.getLogger("client")
    logger.setLevel(logging.ERROR)
    return pulsar.Client(f"pulsar://pulsar:6650", logger=logger)


class Despachador:
    def __init__(self):
        self.logger = logger.getChild("despachador")

    def _publicar_mensaje(self, topico: str, mensaje: schema.Record):
        cliente = get_pulsar_client()
        publicador = cliente.create_producer(
            topico, schema=schema.AvroSchema(mensaje.__class__)  # pyright: ignore
        )
        publicador.send(mensaje)
        self.logger.info(f"Publicado {type(mensaje).__name__} en el topico {topico}")
        cliente.close()

    def publicar_evento(self, evento: EventoIntegracion):
        self._publicar_mensaje(topico=evento.topic_name(), mensaje=evento)

    def publicar_comando(self, comando: Comando):
        self._publicar_mensaje(topico=comando.topic_name(), mensaje=comando)


despachador = Despachador()


def comenzar_despachador_eventos_integracion_a_pulsar():
    dispatcher.connect(despachador.publicar_evento, signal="Integracion")


def comenzar_despachador_coamndos_a_pulsar():
    dispatcher.connect(despachador.publicar_comando, signal="Comando")


class Consumidor:
    mensaje: type[EventoIntegracion] | type[Comando]
    topico: str
    handler: Callable
    tipo: str

    def __init__(
        self,
        mensaje: type[EventoIntegracion] | type[Comando],
        handler: Callable,
    ):
        self.topico = mensaje().topic_name()
        self.mensaje = mensaje
        self.handler = handler

        if issubclass(mensaje, EventoIntegracion):
            self.tipo = "evento"
        elif issubclass(mensaje, Comando):
            self.tipo = "comando"
        else:
            self.tipo = "desconocido"

        self.logger = logger.getChild(self.name())

    def name(self):
        return f"consumidor-{self.tipo}-topico-{self.topico}"

    def start(self):
        self.logger.info(f"Comenzando a consumir del topico {self.topico}")
        cliente = get_pulsar_client()
        consumidor = cliente.subscribe(
            self.topico,
            consumer_type=pulsar.ConsumerType.Shared,
            subscription_name="sub",
            schema=schema.AvroSchema(self.mensaje),  # pyright: ignore
        )
        while True:
            res = consumidor.receive()
            self.logger.info(f"Recibido mensaje del topico {self.topico}")
            value = res.value()
            self.logger.info(
                f"Mensaje deserializado de tipo {value.__class__.__name__} del topico {self.topico}"
            )
            self.handler(value)
            consumidor.acknowledge(res)
            self.logger.info(
                f"Acknowledged mensaje {value.__class__.__name__} del topico {self.topico}"
            )
