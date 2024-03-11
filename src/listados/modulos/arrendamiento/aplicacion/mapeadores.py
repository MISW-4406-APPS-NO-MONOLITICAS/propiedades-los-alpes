import uuid
from listados.seedwork.dominio.repositorios import Mapeador
from listados.modulos.arrendamiento.dominio.entidades import Arrendamiento
from listados.modulos.arrendamiento.aplicacion.dto import ArrendamientoDTO
from .dto import ArrendamientoDTO


class MapeadorArrendamientoDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> ArrendamientoDTO:
        return ArrendamientoDTO(
            id_correlacion=externo["id_correlacion"],
            id_propiedad=externo["id_propiedad"],
            id_transaccion=externo["id_transaccion"],
            fecha_evento=externo["fecha_evento"],
            valor=externo["valor"],
            inquilino=externo["inquilino"],
            arrendatario=externo["arrendatario"]    
        )

    def dto_a_externo(self, dto: ArrendamientoDTO) -> dict:
        return {
            "id_correlacion": dto.id_correlacion,
            "id_propiedad": dto.id_propiedad,
            "id_transaccion": dto.id_transaccion,
            "fecha_evento": dto.fecha_evento,
            "valor": dto.valor,
            "inquilino": dto.inquilino,
            "arrendatario": dto.arrendatario, 
        }

    def dto_a_entidad(self, dto):
        raise NotImplementedError
    
    def entidad_a_dto(self, entidad):
        raise NotImplementedError
    
class MapeadorArrendamiento(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"

    def entidad_a_dto(self, entidad: Arrendamiento) -> ArrendamientoDTO:
        id_correlacion = entidad.id_correlacion
        id_propiedad = entidad.id_propiedad
        id_transaccion = entidad.id_transaccion
        fecha_evento = entidad.fecha_creacion
        valor = entidad.valor
        inquilino = entidad.inquilino
        arrendatario = entidad.arrendatario
        return ArrendamientoDTO(
            id_correlacion=id_correlacion,
            id_propiedad=id_propiedad,
            id_transaccion=id_transaccion,
            fecha_evento= fecha_evento,
            valor=valor,
            inquilino=inquilino,
            arrendatario=arrendatario,
        )
        
        
    
    def dto_a_entidad(self, dto: ArrendamientoDTO) -> Arrendamiento:
        return Arrendamiento(
            id_correlacion=dto.id_correlacion,
            id_propiedad=dto.id_propiedad,
            id_transaccion=dto.id_transaccion,
            fecha_evento=dto.fecha_evento,
            valor=dto.valor,
            inquilino=dto.inquilino,
            arrendatario=dto.arrendatario,
        )