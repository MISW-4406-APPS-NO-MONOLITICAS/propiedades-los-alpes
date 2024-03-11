from dataclasses import dataclass, field
from listados.seedwork.aplicacion.dto import DTO
from datetime import datetime


@dataclass(frozen=True)
class ArrendamientoDTO(DTO):
    id_correlacion: str = field(default_factory=str)
    id_propiedad: str = field(default_factory=str)
    id_transaccion: str = field(default_factory=str)
    fecha_evento: datetime = field(default_factory=datetime.now)
    valor: float = field(default_factory=float)
    inquilino: str = field(default_factory=str)
    arrendatario: str = field(default_factory=str)

