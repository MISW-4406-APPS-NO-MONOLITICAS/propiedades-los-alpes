""" Mapeadores para la capa de infrastructura del dominio de contratos
"""

from listados.seedwork.dominio.repositorios import Mapeador
from listados.modulos.contratos.dominio.objetos_valor import FechaInicio, FechaVencimiento, Valor, NoticiaMedio, MaterialMercado
from listados.modulos.contratos.dominio.entidades import Transaccion, Venta, Alquiler, Listado, Subarrendamiento, TrabajoConjunto
from .dto import TransaccionDB

class MapeadorTransaccion(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%d %H:%M:%S'

    def obtener_tipo(self) -> type:
        return Transaccion.__class__

    def dto_a_entidad(self, dto: TransaccionDB) -> Transaccion:
        return Transaccion(
            id=dto.id,
            fecha_creacion=dto.fecha_creacion,
            fecha_actualizacion=dto.fecha_actualizacion,
            valor=Valor(valor=dto.valor),
            comprador=dto.comprador,
            vendedor=dto.vendedor,
            inquilino=dto.inquilino,
            arrendatario=dto.arrendatario
        )
    
    def entidad_a_dto(self, entidad: Transaccion) -> TransaccionDB:
        return TransaccionDB(
            id=entidad.id,
            fecha_creacion=entidad.fecha_creacion.strftime(self._FORMATO_FECHA),
            fecha_actualizacion=entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA),
            valor=entidad.valor.valor,
            comprador=entidad.comprador,
            vendedor=entidad.vendedor,
            inquilino=entidad.inquilino,
            arrendatario=entidad.arrendatario
        )