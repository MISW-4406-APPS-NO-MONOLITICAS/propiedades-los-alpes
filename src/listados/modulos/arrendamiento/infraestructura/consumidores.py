from listados.config.pulsar import Consumidor
from listados.modulos.arrendamiento.aplicacion.comandos.arrendar_propiedad import (
    ComandoArrendarPropiedad,
    ComandoArrendarPropiedadHandler
)


consumidores_arrendamiento = [
    Consumidor(
        topico=ComandoArrendarPropiedad().topic_name(),
        mensaje=ComandoArrendarPropiedad,# type: ignore
        handler=ComandoArrendarPropiedadHandler,
    ).start 
]
