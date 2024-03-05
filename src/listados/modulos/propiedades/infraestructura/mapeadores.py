""" Mapeadores para la capa de infrastructura del dominio de contratos
"""

import uuid
from listados.seedwork.dominio.repositorios import Mapeador
from listados.modulos.propiedades.dominio.objetos_valor import (
    Valor,
)
from listados.modulos.propiedades.dominio.entidades import (
    Propiedad,
)
from .dto import PropiedadDB


class MapeadorPropiedadDB(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

    def dto_a_entidad(self, dto: PropiedadDB) -> Propiedad:
        return Propiedad(
            id=uuid.UUID(dto.id),
           
            tipo_construccion=dto.tipo_construccion,
            estado=dto.estado,
            area=dto.area,
            direccion=dto.direccion,
            lote=dto.lote,
            compania=dto.compania,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion
        )

    def entidad_a_dto(self, entidad: Propiedad) -> PropiedadDB:
        return PropiedadDB(
            id=str(entidad.id),
            fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA),
            fecha_actualizacion=entidad.fecha_actualizacion.strftime(
                self._FORMATO_FECHA
            ),
            tipo_construccion=entidad.tipo_construccion,
            estado=entidad.estado,
            area=entidad.area,
            direccion=entidad.direccion,
            lote=entidad.lote,
            compania=entidad.compania

        )
