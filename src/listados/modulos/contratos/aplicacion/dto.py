from dataclasses import dataclass, field
from listados.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class Valor(DTO):
    valor: float


@dataclass(frozen=True)
class TransaccionDto(DTO):
    id: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    valor: Valor = field(default_factory=float)
    comprador: str = field(default_factory=str)
    vendedor: str = field(default_factory=str)
    inquilino: str = field(default_factory=str)
    arrendatario: str = field(default_factory=str)

"""

@dataclass(frozen=True)
class VentaDto(TransaccionDto):
    comprador: str = field(default_factory=str)
    vendedor: str = field(default_factory=str)

@dataclass(frozen=True)
class AlquilerDto(TransaccionDto):
    inquilino: str = field(default_factory=str)
    arrendatario: str = field(default_factory=str)
"""