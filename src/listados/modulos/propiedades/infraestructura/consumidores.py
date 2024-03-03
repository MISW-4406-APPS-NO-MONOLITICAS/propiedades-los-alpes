from listados.config.pulsar import Consumidor
from listados.modulos.propiedades.aplicacion.comandos.crear_propiedad import (
    ComandoCrearPropiedad,
    ComandoCrearPropiedadHandler,
)
from listados.modulos.propiedades.aplicacion.handlers import (
    PropiedadCreadaIntegracionHandler,
)
from listados.modulos.propiedades.dominio.eventos import PropiedadCreadaIntegracion


consumidores_propiedades = [
    Consumidor(
        topico=PropiedadCreadaIntegracion().topic_name(),
        mensaje=PropiedadCreadaIntegracion, # type: ignore
        handler=PropiedadCreadaIntegracionHandler,
    ).start,
    Consumidor(
        topico=ComandoCrearPropiedad().topic_name(),
        mensaje=ComandoCrearPropiedad, # type: ignore
        handler=ComandoCrearPropiedadHandler().handle,
    ).start
]
