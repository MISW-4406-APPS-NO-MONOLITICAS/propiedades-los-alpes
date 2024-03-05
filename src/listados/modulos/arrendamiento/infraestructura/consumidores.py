from listados.config.pulsar import Consumidor
from listados.modulos.arrendamiento.aplicacion.handlers import (
    ContratoPropiedadArrendadaIntegracionHandler,
)
from listados.modulos.arrendamiento.dominio.eventos import ContratoPropiedadArrendadaIntegracion


consumidores_arrendamiento = [
    Consumidor(
        topico=ContratoPropiedadArrendadaIntegracion().topic_name(),
        mensaje=ContratoPropiedadArrendadaIntegracion, # type: ignore
        handler=ContratoPropiedadArrendadaIntegracionHandler,
    ).start,
    
]
