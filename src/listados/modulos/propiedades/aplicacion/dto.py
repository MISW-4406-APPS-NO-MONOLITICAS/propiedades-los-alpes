from dataclasses import dataclass, field
from listados.seedwork.aplicacion.dto import DTO

@dataclass(frozen=True)
class CrearPropiedadDTO(DTO):
    id: str = field(default_factory=str)
    nombre: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)