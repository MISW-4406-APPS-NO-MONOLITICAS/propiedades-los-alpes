from dataclasses import dataclass, field
from listados.seedwork.aplicacion.dto import DTO
from listados.modulos.propiedades.dominio.objetos_valor import Valor

@dataclass(frozen=True)
class PropiedadDTO(DTO):
    id: str = field(default_factory=str)
    tipo_construccion: str = field(default_factory=str)
    estado: bool = field(default_factory=bool)
    area: float = field(default_factory=float)
    direccion: str = field(default_factory=str)
    lote: int = field(default_factory=int)
    compania: str = field(default_factory=str)
    fecha_registro: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)

@dataclass(frozen=True)
class ActualizarPropiedadDTO(DTO):
    id: str = field(default_factory=str)
    estado: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)






