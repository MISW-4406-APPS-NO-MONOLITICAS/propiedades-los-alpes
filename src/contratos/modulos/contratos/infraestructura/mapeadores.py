""" Mapeadores para la capa de infrastructura del dominio de contratos
"""

import uuid
from contratos.seedwork.dominio.repositorios import Mapeador
from contratos.modulos.contratos.dominio.objetos_valor import (
    Valor,
)
from contratos.modulos.contratos.dominio.entidades import (
    Transaccion,
)
from .dto import TransaccionDB


class MapeadorTransaccionDB(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

    def dto_a_entidad(self, dto: TransaccionDB) -> Transaccion:
        return Transaccion(
            id=uuid.UUID(dto.id),
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            valor=Valor(valor=dto.valor),
            comprador=dto.comprador,
            vendedor=dto.vendedor,
            inquilino=dto.inquilino,
            arrendatario=dto.arrendatario,
        )

    def entidad_a_dto(self, entidad: Transaccion) -> TransaccionDB:
        return TransaccionDB(
            id=str(entidad.id),
            fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA),
            fecha_actualizacion=entidad.fecha_actualizacion.strftime(
                self._FORMATO_FECHA
            ),
            valor=entidad.valor.valor,
            comprador=entidad.comprador,
            vendedor=entidad.vendedor,
            inquilino=entidad.inquilino,
            arrendatario=entidad.arrendatario,
        )
