from __future__ import annotations
from dataclasses import dataclass, field
import uuid

from listados.seedwork.dominio.eventos import EventoDominio, EventoIntegracion
from datetime import datetime
import pulsar.schema as schema


@dataclass
class ArrendamientoRealizado(EventoDominio):
    id_correlacion: str = field(default_factory=str)
    id_propiedad: str = field(default_factory=str)
    id_transaccion: str = field(default_factory=str)
    arrendamiento_confirmado: bool = field(default_factory=bool)

    
class ContratoPropiedadArrendada(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    id_transaccion = schema.String(required=True)
    fecha_evento = schema.String(required=True)

    def topic_name(self) -> str:
        return "contrato_propiedad_arrendada"