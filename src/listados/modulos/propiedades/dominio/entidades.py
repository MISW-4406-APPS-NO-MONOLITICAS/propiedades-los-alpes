from __future__ import annotations
from datetime import datetime
from listados.config.logger import logger
from dataclasses import dataclass, field
from uuid import uuid4
from datetime import datetime

from listados.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from listados.modulos.propiedades.dominio.eventos import (
    PropiedadArrendamientoRechazadoIntegracion,
    PropiedadArrendadaIntegracion,
)


@dataclass
class Propiedad(AgregacionRaiz):
    id_propiedad: str = field(default_factory=str)
    tipo_construccion: str = field(default_factory=str)
    estado: bool = field(default_factory=bool)
    area: float = field(default_factory=float)
    direccion: str = field(default_factory=str)
    lote: int = field(default_factory=int)
    compania: str = field(default_factory=str)
    fecha_registro: datetime = field(default_factory=datetime.today)
    fecha_actualizacion: datetime = field(default_factory=datetime.today)

    def actualizar_propiedad(
        self, id_propiedad: str, id_correlacion: str, id_transaccion: str
    ):
        logger.info(
            f"Propiedad arrendada, agregando evento de integracion {PropiedadArrendadaIntegracion.__name__}"
        )
        self.agregar_evento_integracion(
            evento=PropiedadArrendadaIntegracion(
                id_correlacion=id_correlacion,
                id_propiedad=id_propiedad,
                id_transaccion=id_transaccion,
            )
        )

        logger.info(
            f"Informacion del evento de integracion: {PropiedadArrendadaIntegracion.__name__} "
            f"id_correlacion: {id_correlacion} "
            f"id_propiedad: {id_propiedad} "
            f"id_transaccion: {id_transaccion} "
        )

    def rechazar_actualizacion_propiedad(
        self, id_propiedad: str, id_correlacion: str, id_transaccion: str
    ):
        logger.info(
            f"Rechazando arrendamiento, agregando evento de integracion {PropiedadArrendamientoRechazadoIntegracion.__name__}"
        )
        self.agregar_evento_integracion(
            PropiedadArrendamientoRechazadoIntegracion(
                id_correlacion=id_correlacion,
                id_propiedad=id_propiedad,
                id_transaccion=id_transaccion,
            )
        )

        logger.info(
            f"Informacion del evento de integracion: {PropiedadArrendamientoRechazadoIntegracion.__name__} "
            f"id_correlacion: {id_correlacion} "
            f"id_propiedad: {id_propiedad} "
            f"id_transaccion: {id_transaccion} "
        )

    def crear_propiedad(
        self,
        id_propiedad: str,
        tipo_construccion: str,
        estado: bool,
        area: float,
        direccion: str,
        lote: int,
        compania: str,
    ):
        self.id_propiedad = id_propiedad
        self.tipo_construccion = tipo_construccion
        self.estado = estado
        self.area = area
        self.direccion = direccion
        self.lote = lote
        self.compania = compania
        self.fecha_registro = datetime.now()
        self.fecha_actualizacion = datetime.now()
        logger.info(
            f"Creando propiedad con id {id_propiedad} y fecha de registro {self.fecha_registro}"
        )
        return self
