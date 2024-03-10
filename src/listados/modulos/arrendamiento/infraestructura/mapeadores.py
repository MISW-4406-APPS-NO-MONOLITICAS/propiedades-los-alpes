import uuid
from listados.seedwork.dominio.repositorios import Mapeador
from listados.modulos.arrendamiento.dominio.entidades import (
    Arrendamiento,
)

from .dto import ArrendamientoDB

class MapeadorArrendamientoDB(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

    def dto_a_entidad(self, dto: ArrendamientoDB) -> Arrendamiento:
        return Arrendamiento(
            id=uuid.UUID(dto.id),
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            id_correlacion=dto.id_correlacion,
            id_propiedad = dto.id_propiedad,
            id_transaccion = dto.id_transaccion,
            fecha_evento = dto.fecha_evento,
            valor = dto.valor,
            inquilino = dto.inquilino,
            arrendatario = dto.arrendatario
        )
    
    def entidad_a_dto(self, entidad: Arrendamiento) -> ArrendamientoDB:
        return ArrendamientoDB(
            id=str(entidad.id),
            fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA),
            fecha_actualizacion=entidad.fecha_actualizacion.strftime(
                self._FORMATO_FECHA
            ),
            id_correlacion=entidad.id_correlacion,
            id_propiedad = entidad.id_propiedad,
            id_transaccion = entidad.id_transaccion,
            fecha_evento = entidad.fecha_evento.strftime(self._FORMATO_FECHA),
            valor = entidad.valor,
            inquilino = entidad.inquilino,
            arrendatario = entidad.arrendatario
        
        )
