from dataclasses import dataclass, field
from listados.seedwork.aplicacion.dto import DTO
from listados.modulos.contratos.dominio.objetos_valor import Valor


@dataclass(frozen=True)
class Valor(DTO):
    valor: float


@dataclass(frozen=True)
class TransaccionDTO(DTO):
    id: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    valor: Valor = field(default_factory=Valor)
    comprador: str = field(default_factory=str)
    vendedor: str = field(default_factory=str)
    inquilino: str = field(default_factory=str)
    arrendatario: str = field(default_factory=str)
