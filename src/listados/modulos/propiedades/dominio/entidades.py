from __future__ import annotations
import datetime
from listados.config.logger import logger
from dataclasses import dataclass, field
from uuid import uuid4
from listados.modulos.propiedades.dominio.objetos_valor import Valor

from listados.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from listados.modulos.propiedades.dominio.eventos import (
    PropiedadCreada,
    PropiedadCreadaIntegracion
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
    fecha_registro: datetime.date = field(default_factory=datetime.date.today)
    fecha_actualizacion: datetime.date = field(default_factory=datetime.date.today)

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

    


