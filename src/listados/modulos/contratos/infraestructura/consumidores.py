from listados.config.pulsar import Consumidor
from listados.modulos.contratos.aplicacion.comandos.crear_transaccion import (
    ComandoCrearTransaccion,
    ComandoCrearTransaccionHandler,
)
from listados.modulos.contratos.aplicacion.handlers import (
    TransaccionCreadaIntegracionHandler,
)
from listados.modulos.contratos.dominio.eventos import TransaccionCreadaIntegracion


consumidores = [
    Consumidor(
        topico=TransaccionCreadaIntegracion().topic_name(),
        mensaje=TransaccionCreadaIntegracion,
        handler=TransaccionCreadaIntegracionHandler,
    ).start,
    Consumidor(
        topico=ComandoCrearTransaccion().topic_name(),
        mensaje=ComandoCrearTransaccion,
        handler=ComandoCrearTransaccionHandler().handle,
    ).start,
]
