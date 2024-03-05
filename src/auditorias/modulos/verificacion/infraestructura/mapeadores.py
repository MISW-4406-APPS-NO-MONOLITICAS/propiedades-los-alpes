# Mapeadores para la capa de infrastructura del dominio de auditorias

import uuid
from auditorias.seedwork.dominio.repositorios import Mapeador
from auditorias.modulos.verificacion.dominio.objetos_valor import (
    TipoAnalisis,
)
from auditorias.modulos.verificacion.dominio.entidades import (
    Analisis,
)
from .dto import AnalisisDB


class MapeadorAnalisisDB(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%d %H:%M:%S"

    def dto_a_entidad(self, dto: AnalisisDB) -> Analisis:
        return Analisis(
            id=uuid.UUID(dto.id),
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            tipo_analisis=TipoAnalisis(valor=dto.tipo_analisis),
            contrato_id=dto.contrato_id,
            oficial=dto.oficial,
            consistente=dto.consistente,
            completo=dto.completo,
            indice_confiabilidad=dto.indice_confiabilidad,
            auditado=dto.auditado,
        )

    def entidad_a_dto(self, entidad: Analisis) -> AnalisisDB:
        return AnalisisDB(
            id=str(entidad.id),
            fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA),
            fecha_actualizacion=entidad.fecha_actualizacion.strftime(
                self._FORMATO_FECHA
            ),
            tipo_analisis=entidad.tipo_analisis.valor,
            contrato_id=entidad.contrato_id,
            oficial=entidad.oficial,
            consistente=entidad.consistente,
            completo=entidad.completo,
            indice_confiabilidad=entidad.indice_confiabilidad,
            auditado=entidad.auditado,
        )
