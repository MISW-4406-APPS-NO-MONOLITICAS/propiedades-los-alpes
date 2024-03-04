from __future__ import annotations
from dataclasses import dataclass, field
import uuid

from listados.seedwork.dominio.eventos import EventoDominio, EventoIntegracion
from datetime import datetime
import pulsar.schema as schema


@dataclass
class PropiedadCreada(EventoDominio):
    id_propiedad: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_registro: datetime = field(default_factory=datetime.now)


class PropiedadCreadaIntegracion(EventoIntegracion):
    id = schema.String(required=True)
    fecha_evento = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    tipo_construccion = schema.String(required=True)
    esta_disponible = schema.Boolean(required=True)
    area = schema.Float(required=True)
    direccion = schema.String(required=True)
    lote = schema.Integer(required=True)
    compania = schema.String(required=True)

    def topic_name(self):
        return "propiedad_creada"
    

@dataclass
class PropiedadActualizada(EventoDominio):
    id_propiedad: uuid.UUID = field(default_factory=uuid.uuid4)
    fecha_actualizacion: datetime = field(default_factory=datetime.now)


class PropiedadActualizadaIntegracion(EventoIntegracion):
    id = schema.String(required=True)
    fecha_evento = schema.String(required=True)
    id_propiedad = schema.String(required=True)
    tipo_construccion = schema.String(required=True)
    esta_disponible = schema.Boolean(required=True)
    area = schema.Float(required=True)
    direccion = schema.String(required=True)
    lote = schema.Integer(required=True)
    compania = schema.String(required=True)

    def topic_name(self):
        return "propiedad_actualizada"