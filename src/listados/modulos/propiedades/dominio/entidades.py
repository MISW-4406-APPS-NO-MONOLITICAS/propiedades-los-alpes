from __future__ import annotations
from datetime import datetime
from listados.config.logger import logger
from dataclasses import dataclass, field
from uuid import uuid4
from listados.modulos.propiedades.dominio.objetos_valor import Valor

from listados.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from listados.modulos.propiedades.dominio.eventos import (
    PropiedadCreada,
    PropiedadCreadaIntegracion,
    PropiedadActualizada,
    PropiedadActualizadaIntegracion,
)
from contratos.seedwork.dominio.eventos import EventoIntegracion


@dataclass
class Propiedad(AgregacionRaiz):
    tipo_construccion: str = field(default_factory=str)
    estado: bool = field(default_factory=bool)
    area: float = field(default_factory=float)
    direccion: str = field(default_factory=str)
    lote: int = field(default_factory=int)
    compania: str = field(default_factory=str)
    fecha_registro: datetime = field(default_factory=datetime.today)
    fecha_actualizacion: datetime = field(default_factory=datetime.today)

    def crear_propiedad(self):
        logger.info(
            f"Creando propiedad, agregando evento de dominio {type(PropiedadCreada).__name__}"
        )
        self.agregar_evento(
            PropiedadCreada(
                id_propiedad=self.id, 
                fecha_registro=self.fecha_creacion
            )
        )

        self.agregar_evento_integracion(
            evento=PropiedadCreadaIntegracion(
                id=str(uuid4()),
                fecha_evento=self.fecha_creacion,
                id_propiedad=str(self.id),
                tipo_construccion=self.tipo_construccion,
                estado=self.estado,
                area=self.area,
                direccion=self.direccion,
                lote=self.lote,
                compania=self.compania,
                fecha_registro=self.fecha_creacion,
                fecha_actualizacion=self.fecha_actualizacion
            )
        )

    def actualizar_propiedad(self):
        logger.info(
            f"Actualizando propiedad, agregando evento de dominio {type(PropiedadCreada).__name__}"
        )
        self.agregar_evento(
            PropiedadActualizada(
                id_propiedad=self.id, 
                fecha_actualizacion=self.fecha_actualizacion
            )

        )

        self.agregar_evento_integracion(
            evento=PropiedadActualizadaIntegracion(
                id=str(uuid4()),
                fecha_evento=self.fecha_actualizacion,
                id_propiedad=str(self.id),
                tipo_construccion=self.tipo_construccion,
                estado=True,
                area=self.area,
                direccion=self.direccion,
                lote=self.lote,
                compania=self.compania,
                fecha_registro=self.fecha_registro,
                fecha_actualizacion=self.fecha_actualizacion
            )
        )

    


