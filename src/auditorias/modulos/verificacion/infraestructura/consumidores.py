from auditorias.config.pulsar import Consumidor
from auditorias.modulos.verificacion.aplicacion.handlers import (
    TransaccionCreadaIntegracionHandler,
)

from auditorias.modulos.verificacion.dominio.eventos import TransaccionCreadaIntegracion


consumidores = [
    Consumidor(
        topico=TransaccionCreadaIntegracion().topic_name(),
        mensaje=TransaccionCreadaIntegracion,  # type: ignore
        handler=TransaccionCreadaIntegracionHandler,
    ).start,
]
