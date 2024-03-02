from listados.config.pulsar import Consumidor
from listados.modulos.propiedades.aplicacion.comandos.crear_transaccion import (
    ComandoCrearTransaccion,
    ComandoCrearTransaccionHandler,
)
from listados.modulos.propiedades.aplicacion.handlers import (
    TransaccionCreadaIntegracionHandler,
)
from listados.modulos.propiedades.dominio.eventos import TransaccionCreadaIntegracion


consumidores = [
    Consumidor(
        topico=TransaccionCreadaIntegracion().topic_name(),
        mensaje=TransaccionCreadaIntegracion, # type: ignore
        handler=TransaccionCreadaIntegracionHandler,
    ).start,
    Consumidor(
        topico=ComandoCrearTransaccion().topic_name(),
        mensaje=ComandoCrearTransaccion, # type: ignore
        handler=ComandoCrearTransaccionHandler().handle,
    ).start,
]
