from __future__ import annotations

from dataclasses import dataclass, field
from listados.seedwork.dominio.objetos_valor import ObjetoValor

@dataclass(frozen=True)
class TipoConstruccion(ObjetoValor):
    ...

@dataclass(frozen=True)
class Minoristas(TipoConstruccion):
    ...


@dataclass(frozen=True)
class UsoEspecializado(TipoConstruccion):
    ...


@dataclass(frozen=True)
class Oficina(TipoConstruccion):
    ...


@dataclass(frozen=True)
class Industrial(TipoConstruccion):
    ...


@dataclass(frozen=True)
class Area(ObjetoValor):
    ...

@dataclass(frozen=True)
class Tamano(ObjetoValor):
    ...

@dataclass(frozen=True)
class CantidadPisos(ObjetoValor):
    ...

@dataclass(frozen=True)
class Estacionamiento(ObjetoValor):
    ...