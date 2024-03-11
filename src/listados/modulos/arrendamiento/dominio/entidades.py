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
from listados.modulos.arrendamiento.dominio.reglas_negocio import ReglaNegocio
@dataclass
class Arrendamiento(AgregacionRaiz):
    id_correlacion: str = field(default_factory=str)
    id_propiedad: str = field(default_factory=str)
    id_transaccion: str = field(default_factory=str)
    fecha_evento: datetime = field(default_factory=datetime.now)
    valor: float = field(default_factory=float)
    inquilino: str = field(default_factory=str)
    arrendatario: str = field(default_factory=str)



    def arrendar_propiedad(self):
        reglas = ReglaNegocio(self.valor)
        logger.info(
            f"Agregando evento de dominio {ArrendamientoRealizado.__name__}"
        )
        self.agregar_evento(
            ArrendamientoRealizado( 
                id_correlacion=self.id_correlacion,
                id_propiedad=self.id_propiedad,
                id_transaccion=self.id_transaccion,
                arrendamiento_confirmado= reglas.validar_monto_arriendo(), 
            )
        )
        
    



    
    


