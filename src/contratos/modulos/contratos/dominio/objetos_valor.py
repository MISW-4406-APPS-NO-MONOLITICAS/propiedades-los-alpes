from __future__ import annotations

from dataclasses import dataclass, field
from contratos.seedwork.dominio.objetos_valor import ObjetoValor


@dataclass(frozen=True)
class FechaInicio(ObjetoValor):
    ...


@dataclass(frozen=True)
class FechaVencimiento(ObjetoValor):
    ...


@dataclass(frozen=True)
class Valor(ObjetoValor):
    valor: float = field(default_factory=float)


@dataclass(frozen=True)
class NoticiaMedio(ObjetoValor):
    ...


@dataclass(frozen=True)
class MaterialMercado(ObjetoValor):
    ...
