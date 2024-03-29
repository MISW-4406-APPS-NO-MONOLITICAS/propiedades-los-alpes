from dataclasses import dataclass, field
from contratos.seedwork.aplicacion.dto import DTO
from contratos.modulos.contratos.dominio.objetos_valor import Valor


@dataclass(frozen=True)
class CrearTransaccionDTO(DTO):
    id_propiedad: str = field(default_factory=str)
    valor: Valor = field(default_factory=Valor)
    comprador: str = field(default_factory=str)
    vendedor: str = field(default_factory=str)
    inquilino: str = field(default_factory=str)
    arrendatario: str = field(default_factory=str)
