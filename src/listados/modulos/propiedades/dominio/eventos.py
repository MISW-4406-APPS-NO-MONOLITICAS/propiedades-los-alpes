from __future__ import annotations
from dataclasses import dataclass, field
import uuid

from listados.seedwork.dominio.eventos import EventoDominio, EventoIntegracion
from datetime import datetime
import pulsar.schema as schema

@dataclass
class PropiedadArrendadaDominio(EventoDominio):
    id_correlacion: str = field(default_factory=str)
    id_transaccion: str = field(default_factory=str)
    id_propiedad: str = field(default_factory=str)
    arrendamiento_confirmado: bool = field(default_factory=bool)


class PropiedadArrendada(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    id_transaccion = schema.String(required=True)

    def topic_name(self) -> str:
        return "listados_propiedad_arrendada"

class PropiedadArrendamientoRechazado(EventoIntegracion):
    id_correlacion = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    id_transaccion = schema.String(required=True)

    def topic_name(self) -> str:
        return "listados_arrendamiento_fallido"