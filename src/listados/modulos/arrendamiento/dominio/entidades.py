from __future__ import annotations
from datetime import datetime
from listados.config.logger import logger
from dataclasses import dataclass, field
from uuid import uuid4

from listados.seedwork.dominio.entidades import AgregacionRaiz, Entidad
from listados.modulos.arrendamiento.dominio.eventos import (
    ArrendamientoRealizado
)
from listados.seedwork.dominio.eventos import EventoIntegracion, EventoDominio

@dataclass
class Arrendamiento(AgregacionRaiz):
    estado: bool = field(default_factory=bool)
    fecha_registro: datetime = field(default_factory=datetime.now)  
    fecha_actualizacion: datetime = field(default_factory=datetime.now)
    

    def crear_arrendamiento(self):
        logger.info(
            f"Creando arrendamiento, agregando evento de dominio {type(ArrendamientoRealizado).__name__}"
        )
        self.agregar_evento(
            ArrendamientoRealizado(
                id_arrendamiento=self.id, 
                fecha_registro=self.fecha_creacion
            )

        )

    



    
    


