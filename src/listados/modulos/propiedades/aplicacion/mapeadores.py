import datetime
from listados.seedwork.dominio.repositorios import Mapeador
from listados.modulos.propiedades.dominio.entidades import Propiedad
from listados.modulos.propiedades.aplicacion.dto import Valor
from .dto import PropiedadDTO


class MapeadorPropiedadDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> PropiedadDTO:
        return PropiedadDTO(
            id="",
            tipo_construccion=externo["tipo_construccion"],
            estado=externo["estado"],
            area=externo["area"],
            direccion=externo["direccion"],
            lote=externo["lote"],
            compania=externo["compania"],
            fecha_registro=externo["fecha_registro"],
            fecha_actualizacion=externo["fecha_actualizacion"]

        )

        

    def dto_a_externo(self, dto: PropiedadDTO) -> dict:
        return {
            "id": dto.id,
            "tipo_construccion": dto.tipo_construccion,
            "estado": dto.estado,
            "area": dto.area,
            "direccion": dto.direccion,
            "lote": dto.lote,
            "compania": dto.compania,
            "fecha_registro": dto.fecha_registro,
            "fecha_actualizacion": dto.fecha_actualizacion,
        }

    def dto_a_entidad(self, dto):
        raise NotImplementedError

    def entidad_a_dto(self, entidad):
        raise NotImplementedError


class MapeadorPropiedad(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"

    def entidad_a_dto(self, entidad: Propiedad) -> PropiedadDTO:
        _id = str(entidad.id)
        tipo_construccion = entidad.tipo_construccion
        estado = entidad.estado
        area = entidad.area
        direccion = entidad.direccion
        lote = entidad.lote
        compania = entidad.compania
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)

        return PropiedadDTO(
            _id,
            tipo_construccion,
            estado,
            area,
            direccion,
            lote,
            compania,
            fecha_creacion,
            fecha_actualizacion
        )

    def dto_a_entidad(self, dto: PropiedadDTO) -> Propiedad:
        return Propiedad(
            tipo_construccion=dto.tipo_construccion,
            estado=dto.estado,
            area=dto.area,
            direccion=dto.direccion,
            lote=dto.lote,
            compania=dto.compania,
            fecha_creacion=datetime.datetime.strptime(dto.fecha_registro, self._FORMATO_FECHA),
            fecha_actualizacion=datetime.datetime.strptime(dto.fecha_actualizacion, self._FORMATO_FECHA)
        )

       
