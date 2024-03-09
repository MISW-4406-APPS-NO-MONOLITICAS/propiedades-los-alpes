from dataclasses import dataclass, field
from auditorias.seedwork.aplicacion.dto import DTO
from auditorias.modulos.verificacion.dominio.objetos_valor import TipoAnalisis, Valor

@dataclass(frozen=True)
class TransaccionDTO(DTO):
    id: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    contrato_id: str = field(default_factory=str)
    valor: Valor = field(default_factory=Valor)
    comprador: str = field(default_factory=str)
    vendedor: str = field(default_factory=str)
    inquilino: str = field(default_factory=str)
    arrendatario: str = field(default_factory=str)

@dataclass(frozen=True)
class AnalisisDTO(DTO):
    id: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    tipo_analisis: TipoAnalisis = field(default_factory=TipoAnalisis)
    contrato_id: str = field(default_factory=str)
    oficial: bool = field(default_factory=bool)
    consistente: bool = field(default_factory=bool)
    completo: bool = field(default_factory=bool)
    indice_confiabilidad: float = field(default_factory=float)
    auditado: bool = field(default_factory=bool)
    
@dataclass(frozen=True)
class CompensacionDTO(DTO):
    id: str = field(default_factory=str)
    fecha_creacion: str = field(default_factory=str)
    fecha_actualizacion: str = field(default_factory=str)
    contrato_id: str = field(default_factory=str)