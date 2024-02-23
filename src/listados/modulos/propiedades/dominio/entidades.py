from __future__ import annotations
from dataclasses import dataclass, field

import listados.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class Propiedad(AgregacionRaiz):
    ...


@dataclass
class Edificio(Entidad):
    ...