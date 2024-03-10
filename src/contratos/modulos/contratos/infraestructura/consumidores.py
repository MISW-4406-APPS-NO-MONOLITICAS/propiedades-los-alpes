from contratos.config.pulsar import Consumidor
from contratos.modulos.contratos.aplicacion.comandos.schemas import (
    ComandoCrearContrato,
)
from contratos.modulos.contratos.aplicacion.comandos.handlers import (
    ComandoCrearContratoHandler,
)
from contratos.modulos.contratos.aplicacion.handlers import (
    TransaccionCreadaIntegracionHandler,
)
from contratos.modulos.contratos.aplicacion.eventos.schemas import (
    TransaccionCreadaIntegracion,
)


consumidores: list[Consumidor] = [
    Consumidor(
        mensaje=TransaccionCreadaIntegracion,  # type: ignore
        handler=TransaccionCreadaIntegracionHandler,
    ),
    Consumidor(
        mensaje=ComandoCrearContrato,  # type: ignore
        handler=ComandoCrearContratoHandler().handle,
    ),
]
