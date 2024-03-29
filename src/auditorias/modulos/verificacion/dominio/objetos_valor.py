from __future__ import annotations

from dataclasses import dataclass, field
from auditorias.seedwork.dominio.objetos_valor import ObjetoValor

@dataclass(frozen=True)
class TipoAnalisis(ObjetoValor):
    valor: str = field(default_factory=str)
    ...

@dataclass(frozen=True)
class Valor(ObjetoValor):
    valor: float = field(default_factory=float)