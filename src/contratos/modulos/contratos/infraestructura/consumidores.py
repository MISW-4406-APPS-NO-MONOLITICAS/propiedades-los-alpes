from contratos.config.pulsar import Consumidor
from contratos.modulos.contratos.aplicacion.comandos.schemas import (
    ComandoCrearContrato,
)
from contratos.modulos.contratos.aplicacion.comandos.handlers import (
    ComandoCrearContratoHandler,
)


consumidores: list[Consumidor] = [
    Consumidor(
        mensaje=ComandoCrearContrato,  # type: ignore
        handler=ComandoCrearContratoHandler().handle,
    ),
]
