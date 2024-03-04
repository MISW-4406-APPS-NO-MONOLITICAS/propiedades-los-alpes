from auditorias.config.pulsar import Consumidor
""" from auditorias.modulos.verificacion.aplicacion.comandos.modificar_contrato import (
    ComandoCrearTransaccion,
    ComandoCrearTransaccionHandler,
) """
from auditorias.modulos.verificacion.aplicacion.handlers import (
    ContratoCreadoIntegracionHandler,
)
from auditorias.modulos.verificacion.dominio.eventos import ContratoCreadoIntegracion


consumidores = [
    Consumidor(
        topico=ContratoCreadoIntegracion().topic_name(),
        mensaje=ContratoCreadoIntegracion,
        handler=ContratoCreadoIntegracionHandler,
    ).start,
    """ Consumidor(
        topico=ComandoCrearTransaccion().topic_name(),
        mensaje=ComandoCrearTransaccion,
        handler=ComandoCrearTransaccionHandler().handle,
    ).start, """
]
