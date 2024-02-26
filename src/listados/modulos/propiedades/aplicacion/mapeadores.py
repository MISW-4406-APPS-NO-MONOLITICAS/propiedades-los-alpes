

from dataclasses import asdict
from listados.modulos.propiedades.aplicacion.dto import CrearPropiedadDTO
from listados.seedwork.aplicacion.dto import Mapeador


class MapeadorPropiedadDTO(Mapeador):

    def externo_a_dto(self, externo: dict) -> CrearPropiedadDTO:
        return CrearPropiedadDTO(
            id=externo['id'],
            nombre=externo['nombre'],
            fecha_actualizacion=externo['fecha_actualizacion'],
            fecha_creacion=externo['fecha_creacion'],
        )
    
    def dto_a_externo(self, dto: CrearPropiedadDTO) -> dict:
        # Dataclass to dict
        return asdict(dto)