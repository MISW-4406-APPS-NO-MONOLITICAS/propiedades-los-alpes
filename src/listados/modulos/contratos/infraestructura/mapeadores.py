""" Mapeadores para la capa de infrastructura del dominio de contratos
"""

from listados.seedwork.dominio.repositorios import Mapeador
from listados.modulos.contratos.dominio.objetos_valor import FechaInicio, FechaVencimiento, Valor, NoticiaMedio, MaterialMercado
from listados.modulos.contratos.dominio.entidades import Transaccion, Venta, Alquiler, Listado, Subarrendamiento, TrabajoConjunto
from .dto import Transaccion as TransaccionDTO

class MapeadorTransaccion(Mapeador):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        return Transaccion.__class__

    def entidad_a_dto(self, entidad: Transaccion) -> TransaccionDTO:
        print('Entidad: ',entidad)
        transaccion_dto = TransaccionDTO()
        transaccion_dto.id = str(entidad.id)
        transaccion_dto.fecha_creacion = entidad.fecha_creacion
        transaccion_dto.fecha_actualizacion = entidad.fecha_actualizacion
        transaccion_dto.valor = 548521.84 #entidad.valor
        transaccion_dto.comprador = "Benito Perez"
        transaccion_dto.vendedor = "Metro Cuadrado SAS"
        #transaccion_dto.inquilino = entidad.inquilino
        #transaccion_dto.arrendatario = entidad.arrendatario

        return transaccion_dto

    def dto_a_entidad(self, dto: TransaccionDTO) -> Transaccion:
        transaccion = Transaccion(
            dto.id, 
            dto.fecha_creacion, 
            dto.fecha_actualizacion,
            dto.valor,
            dto.comprador,
            dto.vendedor,
            dto.inquilino,
            dto.arrendatario
        )
        
        return transaccion