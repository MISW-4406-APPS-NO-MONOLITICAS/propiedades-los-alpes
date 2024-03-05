from dataclasses import dataclass, field
from listados.seedwork.aplicacion.dto import DTO


@dataclass(frozen=True)
class ArrendamientoDTO(DTO):
    tipo_construccion: str = field(default_factory=str)
    estado: bool = field(default_factory=bool)
    area: float = field(default_factory=float)
    direccion: str = field(default_factory=str)
    lote: int = field(default_factory=int)
    compania: str = field(default_factory=str)
    fecha_registro: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)

