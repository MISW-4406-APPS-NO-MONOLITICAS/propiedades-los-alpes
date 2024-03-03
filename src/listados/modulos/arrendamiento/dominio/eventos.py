from __future__ import annotations
from dataclasses import dataclass, field
import uuid

from listados.seedwork.dominio.eventos import EventoDominio, EventoIntegracion
from datetime import datetime
import pulsar.schema as schema


@dataclass
class ArrendamientoRealizado(EventoDominio):
    id_arrendamiento: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_registro: datetime = field(default_factory=datetime.now)
    

class ContratoPropiedadArrendadaIntegracion(EventoIntegracion):
    id = schema.String(required=True)
    fecha_evento = schema.String(required=True)
    id_arrendamiento = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    estado = schema.String(required=True)
    fecha_registro = schema.String(required=True)

    def topic_name(self):
        return "contrato_propiedad_arrendado"
    


