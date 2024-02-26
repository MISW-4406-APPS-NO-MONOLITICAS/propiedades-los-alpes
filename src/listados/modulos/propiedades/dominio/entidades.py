from __future__ import annotations
from dataclasses import dataclass, field
from enum import nonmember

from listados.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class Propiedad(AgregacionRaiz):
    nombre: str

@dataclass
class Edificio(Entidad):
    ...