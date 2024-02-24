from __future__ import annotations
from dataclasses import dataclass, field

from listados.seedwork.dominio.entidades import AgregacionRaiz, Entidad

@dataclass
class Transaccion(AgregacionRaiz):
    ...

@dataclass
class Venta(Entidad):
    ...

@dataclass
class Alquiler(Entidad):
    ...

@dataclass
class Listado(Entidad):
    ...

@dataclass
class Subarrendamiento(Entidad):
    ...

@dataclass
class TrabajoConjunto(Entidad):
    ...
    