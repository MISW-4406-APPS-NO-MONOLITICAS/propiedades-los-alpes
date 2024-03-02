from contratos.config.pulsar import Consumidor
from contratos.modulos.contratos.aplicacion.comandos.crear_transaccion import (
    ComandoCrearTransaccion,
    ComandoCrearTransaccionHandler,
)
from contratos.modulos.contratos.aplicacion.handlers import (
    TransaccionCreadaIntegracionHandler,
)
from contratos.modulos.contratos.dominio.eventos import TransaccionCreadaIntegracion


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
