import random
import uuid
from listados.modulos.propiedades.dominio.eventos import  PropiedadArrendadaDominio
from listados.config.logger import logger
from listados.seedwork.aplicacion.handlers import Handler
from listados.modulos.propiedades.infraestructura.repositorios import (
    RepositorioPropiedadesDB,
)
from listados.modulos.propiedades.dominio.entidades import Propiedad
from pydispatch import dispatcher


class HandlerPropiedadDominio(Handler):
    def __init__(self, repositorio: RepositorioPropiedadesDB):
        self.repositorio = repositorio

    @staticmethod
    def handler_propiedad_arrendada(evento: PropiedadArrendadaDominio):
        logger.info(
            f"Manejando evento de dominio {type(evento).__name__}"
        )
        propiedad = Propiedad()
        if evento.arrendamiento_confirmado:
            logger.info(
                "Arrendamiento confirmado, actualizando propiedad"
            )
        
            propiedad.actualizar_propiedad(evento.id_propiedad, evento.id_correlacion, evento.id_transaccion)

        else:
            logger.info(
                "Arrendamiento rechazado"
            )
            propiedad.rechazar_actualizacion_propiedad(evento.id_propiedad, evento.id_correlacion, evento.id_transaccion)
            

        
def registrar():
    dispatcher.connect(
        HandlerPropiedadDominio.handler_propiedad_arrendada,
        signal="ArrendamientoRealizadoDominio"
    )