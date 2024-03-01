from listados.config.pulsar import Consumidor
from listados.modulos.contratos.aplicacion.handlers import (
    TransaccionCreadaIntegracionHandler,
)
from listados.modulos.contratos.dominio.eventos import TransaccionCreadaIntegracion


consumidores = [
    Consumidor(
        topico=TransaccionCreadaIntegracion.topic_name(),
        mensaje=TransaccionCreadaIntegracion,
        handler=TransaccionCreadaIntegracionHandler,
    ).start,
]
