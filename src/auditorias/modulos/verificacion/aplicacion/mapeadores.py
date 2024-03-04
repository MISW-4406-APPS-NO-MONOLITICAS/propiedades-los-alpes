from auditorias.modulos.verificacion.dominio.objetos_valor import TipoAnalisis
from auditorias.seedwork.dominio.repositorios import Mapeador
from auditorias.modulos.verificacion.dominio.entidades import Analisis
from .dto import AnalisisDTO


class MapeadorAnalisisDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> AnalisisDTO:
        analisis_dto = AnalisisDTO(
            id="",
            fecha_creacion="",
            fecha_actualizacion="",
            tipo_analisis=TipoAnalisis(externo["tipo_analisis"]),
            contrato_id=externo["contrato_id"],
            oficial=externo["oficial"],
            consistente=externo["consistente"],
            completo=externo["completo"],
            indice_confiabilidad=externo["indice_confiabilidad"],
        )
        return analisis_dto

    def dto_a_externo(self, dto: AnalisisDTO) -> dict:
        return {
            "id": dto.id,
            "fecha_creacion": dto.fecha_creacion,
            "fecha_actualizacion": dto.fecha_actualizacion,
            "tipo_analisis": dto.tipo_analisis.valor,
            "contrato_id": dto.contrato_id,
            "oficial": dto.oficial,
            "consistente": dto.consistente,
            "completo": dto.completo,
            "indice_confiabilidad": dto.indice_confiabilidad,
        }

    def dto_a_entidad(self, dto):
        raise NotImplementedError

    def entidad_a_dto(self, entidad):
        raise NotImplementedError


class MapeadorAnalisis(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"

    def entidad_a_dto(self, entidad: Analisis) -> AnalisisDTO:
        _id = str(entidad.id)
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        tipo_analisis = entidad.tipo_analisis.valor
        contrato_id = entidad.contrato_id
        oficial = entidad.oficial
        consistente = entidad.consistente
        completo = entidad.completo
        indice_confiabilidad = entidad.indice_confiabilidad
        return AnalisisDTO(
            _id,
            fecha_creacion,
            fecha_actualizacion,
            TipoAnalisis(tipo_analisis),
            contrato_id,
            oficial,
            consistente,
            completo,
            indice_confiabilidad,
        )

    def dto_a_entidad(self, dto: AnalisisDTO) -> Analisis:
        analisis = Analisis(
            tipo_analisis=TipoAnalisis(dto.tipo_analisis.valor),
            contrato_id=dto.contrato_id,
            oficial=dto.oficial,
            consistente=dto.consistente,
            completo=dto.completo,
            indice_confiabilidad=dto.indice_confiabilidad,
        )

        return analisis
