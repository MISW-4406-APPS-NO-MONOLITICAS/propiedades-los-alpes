from datetime import datetime
import logging
import os
from typing import Callable
import pulsar
import pulsar.schema as schema
from pydispatch import dispatcher
from auditorias.config.logger import logger
from auditorias.seedwork.aplicacion.comandos import Comando
from auditorias.seedwork.infraestructura.eventos import EventoIntegracion

pulsar_host = os.environ.get("PULSAR_HOST")
if not pulsar_host:
    pulsar_host = "//pulsar:6650"
logger = logging.getLogger("pulsar")

def get_pulsar_client() -> pulsar.Client:
    logger = logging.getLogger("pulsar_client")
    logger.setLevel(logging.ERROR)
    return pulsar.Client(f"pulsar:{pulsar_host}", logger=logger)


class Despachador:
    def __init__(self):
        self.logger = logger.getChild("despachador")

    def _publicar_mensaje(self, topico: str, evento: schema.Record):
        cliente = get_pulsar_client()
        self.logger.info(f"Publicando {type(evento).__name__} en el topico {topico}")
        publicador = cliente.create_producer(
            topico, schema=schema.AvroSchema(evento.__class__)  # pyright: ignore
        )
        instant = datetime.now()
        publicador.send(evento)
        # logger.info(
        #     f"EXPERIMENT - FINAL: id_transaccion: {evento.id_transaccion}, fin-proceso: {instant.isoformat()}, fin-evento: {datetime.now().isoformat()}"
        # )
        self.logger.info(f"Publicado {type(evento).__name__} en el topico {topico}")
        cliente.close()

    def publicar_evento(self, evento: EventoIntegracion):
        self._publicar_mensaje(evento.topic_name(), evento)

    def publicar_comando(self, comando: Comando):
        self._publicar_mensaje(comando.topic_name(), comando)


despachador = Despachador()


def comenzar_despachador_eventos_integracion_a_pulsar():
    dispatcher.connect(despachador.publicar_evento, signal="Integracion")


def comenzar_despachador_comandos_a_pulsar():
    dispatcher.connect(despachador.publicar_comando, signal="Comando")


class Consumidor:
    mensaje: EventoIntegracion | Comando
    topico: str
    handler: Callable

    def __init__(self, topico: str, mensaje: EventoIntegracion | Comando, handler: Callable):
        self.topico = topico
        self.mensaje = mensaje
        self.handler = handler
        self.logger = logger.getChild("consumidor")

    def start(self):
        self.logger.info(f"Comenzando consumo del topico {self.topico}")
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
