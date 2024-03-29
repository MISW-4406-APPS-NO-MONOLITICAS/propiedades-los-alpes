from auditorias.modulos.verificacion.dominio.objetos_valor import TipoAnalisis, Valor
from auditorias.seedwork.dominio.repositorios import Mapeador
from auditorias.modulos.verificacion.dominio.entidades import Analisis
from .dto import AnalisisDTO, CompensacionDTO, TransaccionDTO


class MapeadorTransaccionDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> TransaccionDTO:
        transaccion_dto = TransaccionDTO(
            id_correlacion = externo["id_correlacion"],
            id_transaccion = externo["id_transaccion"],
            valor = Valor(externo["valor"]),
            comprador = externo["comprador"],
            vendedor = externo["vendedor"],
            inquilino = externo["inquilino"],
            arrendatario = externo["arrendatario"],
        )
        return transaccion_dto
      
    def dto_a_entidad(self, dto):
        raise NotImplementedError

    def entidad_a_dto(self, entidad):
        raise NotImplementedError
      
      
class MapeadorCompensacionDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> CompensacionDTO:
        compensacion_dto = CompensacionDTO(
            id_correlacion = externo["id_correlacion"],
            id_transaccion = externo["id_transaccion"],
            id_auditoria = externo["id_auditoria"],
        )
        return compensacion_dto
      
    def dto_a_entidad(self, dto):
        raise NotImplementedError

    def entidad_a_dto(self, entidad):
        raise NotImplementedError


class MapeadorAnalisisDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> AnalisisDTO:
        analisis_dto = AnalisisDTO(
            id = "",
            fecha_creacion = "",
            fecha_actualizacion = "",
            tipo_analisis = TipoAnalisis(externo["tipo_analisis"]),
            id_correlacion = externo["id_correlacion"],
            id_transaccion = externo["id_transaccion"],
            oficial = externo["oficial"],
            consistente = externo["consistente"],
            completo = externo["completo"],
            indice_confiabilidad = externo["indice_confiabilidad"],
            auditado = externo["auditado"],
        )
        return analisis_dto

    def dto_a_externo(self, dto: AnalisisDTO) -> dict:
        return {
            "id": dto.id,
            "fecha_creacion": dto.fecha_creacion,
            "fecha_actualizacion": dto.fecha_actualizacion,
            "tipo_analisis": dto.tipo_analisis.valor,
            "id_correlacion": dto.id_correlacion,
            "id_transaccion": dto.id_transaccion,
            "oficial": dto.oficial,
            "consistente": dto.consistente,
            "completo": dto.completo,
            "indice_confiabilidad": dto.indice_confiabilidad,
            "auditado": dto.auditado,
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
        id_correlacion = entidad.id_correlacion
        id_transaccion = entidad.id_transaccion
        oficial = entidad.oficial
        consistente = entidad.consistente
        completo = entidad.completo
        indice_confiabilidad = entidad.indice_confiabilidad
        auditado = entidad.auditado
        return AnalisisDTO(
            _id,
            fecha_creacion,
            fecha_actualizacion,
            TipoAnalisis(tipo_analisis),
            id_correlacion,
            id_transaccion,
            oficial,
            consistente,
            completo,
            indice_confiabilidad,
            auditado,
        )

    def dto_a_entidad(self, dto: AnalisisDTO) -> Analisis:
        analisis = Analisis(
            tipo_analisis = TipoAnalisis(dto.tipo_analisis.valor),
            id_correlacion = dto.id_correlacion,
            id_transaccion = dto.id_transaccion,
            oficial = dto.oficial,
            consistente = dto.consistente,
            completo = dto.completo,
            indice_confiabilidad = dto.indice_confiabilidad,
            auditado = dto.auditado,
        )

        return analisis
