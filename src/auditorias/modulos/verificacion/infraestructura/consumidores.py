from auditorias.config.pulsar import Consumidor
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
    
]
