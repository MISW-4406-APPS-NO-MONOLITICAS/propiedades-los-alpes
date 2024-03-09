from contratos.config.pulsar import Consumidor
from contratos.modulos.contratos.aplicacion.comandos.crear_contrato import (
    ComandoCrearContrato,
    ComandoCrearContratoHandler,
)
from contratos.modulos.contratos.aplicacion.comandos.crear_transaccion import (
    ComandoCrearTransaccion,
    ComandoCrearTransaccionHandler,
)
from contratos.modulos.contratos.aplicacion.handlers import (
    TransaccionCreadaIntegracionHandler,
)
from contratos.modulos.contratos.dominio.eventos import TransaccionCreadaIntegracion


consumidores: list[Consumidor] = [
    Consumidor(
        topico=TransaccionCreadaIntegracion().topic_name(),
        mensaje=TransaccionCreadaIntegracion,  # type: ignore
        handler=TransaccionCreadaIntegracionHandler,
    ),
    Consumidor(
        topico=ComandoCrearTransaccion().topic_name(),
        mensaje=ComandoCrearTransaccion,  # type: ignore
        handler=ComandoCrearTransaccionHandler().handle,
    ),
    Consumidor(
        topico=ComandoCrearContrato().topic_name(),
        mensaje=ComandoCrearContrato,  # type: ignore
        handler=ComandoCrearContratoHandler().handle,
    ),
]
