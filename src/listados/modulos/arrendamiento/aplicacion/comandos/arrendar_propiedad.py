from dataclasses import dataclass, field
from datetime import datetime
from listados.config.logger import logger
from .base import BaseHandler
from listados.seedwork.aplicacion.comandos import Comando
from listados.seedwork.aplicacion.comandos import ejecutar_commando as comando
from listados.seedwork.infraestructura.uow import UnidadTrabajoPuerto
from listados.modulos.arrendamiento.aplicacion.dto import ArrendamientoDTO
from listados.modulos.arrendamiento.aplicacion.fabricas import FabricaArrendamientos
import pulsar.schema as schema
from datetime import datetime


class ComandoArrendarPropiedad(Comando):
    id_correlacion = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    valor = schema.Float(required=True)
    comprador = schema.String()
    vendedor = schema.String()
    inquilino = schema.String()
    arrendatario = schema.String()

    def topic_name(self) -> str:
        return "listados_arrendar_propiedad"
    


class ComandoArrendarPropiedadHandler(BaseHandler):
    def handle(self, comando: ComandoArrendarPropiedad):
        logger.info(f"Manejando comando {comando.__class__.__name__}")
        arrendamiento_dto = ArrendamientoDTO(
            id_correlacion=str(comando.id_correlacion),
            id_transaccion=str(comando.id_transaccion),
            id_propiedad=str(comando.id_propiedad),
            valor=float(comando.valor),
            inquilino=str(comando.inquilino),
            arrendatario=str(comando.arrendatario),
        )
        arrendamiento = self.fabrica_arrendamientos.crear_objeto(arrendamiento_dto)
        arrendamiento.arrendar_propiedad()  # Genera los eventos

        # Se programa en el uow
        logger.info(f"Inscribiendo en unidad de trabajo del comando {comando.__class__.__name__}")
        UnidadTrabajoPuerto.registrar_batch(
            self.repositorio_arrendamientos.agregar, arrendamiento
        )
        UnidadTrabajoPuerto.savepoint()
        UnidadTrabajoPuerto.commit()


@comando.register(ComandoArrendarPropiedad)
def ejecutar_comando_arrendar_propiedad(comando: ComandoArrendarPropiedad):
    handler = ComandoArrendarPropiedadHandler()
    handler.handle(comando)
