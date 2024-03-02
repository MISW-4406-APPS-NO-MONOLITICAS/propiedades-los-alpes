from listados.seedwork.dominio.repositorios import Mapeador
from listados.modulos.propiedades.dominio.entidades import Transaccion
from listados.modulos.propiedades.aplicacion.dto import Valor
from .dto import PropiedadDTO


class MapeadorPropiedadDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> PropiedadDTO:
        transaccion_dto = PropiedadDTO(
            id="",
            fecha_creacion="",
            fecha_actualizacion="",
            valor=Valor(externo["valor"]),
            comprador=externo["comprador"],
            vendedor=externo["vendedor"],
            inquilino=externo["inquilino"],
            arrendatario=externo["arrendatario"],
        )
        return transaccion_dto

    def dto_a_externo(self, dto: PropiedadDTO) -> dict:
        return {
            "id": dto.id,
            "fecha_creacion": dto.fecha_creacion,
            "fecha_actualizacion": dto.fecha_actualizacion,
            "valor": dto.valor.valor,
            "comprador": dto.comprador,
            "vendedor": dto.vendedor,
            "inquilino": dto.inquilino,
            "arrendatario": dto.arrendatario,
        }

    def dto_a_entidad(self, dto):
        raise NotImplementedError

    def entidad_a_dto(self, entidad):
        raise NotImplementedError


class MapeadorTransaccion(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"

    def entidad_a_dto(self, entidad: Propiedad) -> PropiedadDTO:
        _id = str(entidad.id)
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        valor = entidad.valor
        comprador = entidad.comprador
        vendedor = entidad.vendedor
        inquilino = entidad.inquilino
        arrendatario = entidad.arrendatario
        return TransaccionDTO(
            _id,
            fecha_creacion,
            fecha_actualizacion,
            Valor(valor.valor),
            comprador,
            vendedor,
            inquilino,
            arrendatario,
        )

    def dto_a_entidad(self, dto: TransaccionDTO) -> Transaccion:
        transaccion = Transaccion(
            comprador=dto.comprador,
            vendedor=dto.vendedor,
            inquilino=dto.inquilino,
            arrendatario=dto.arrendatario,
        )

        return transaccion
