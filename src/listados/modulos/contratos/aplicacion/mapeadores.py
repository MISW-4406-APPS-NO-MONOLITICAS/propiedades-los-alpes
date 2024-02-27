from datetime import datetime

from listados.seedwork.aplicacion.dto import Mapeador as AppMap
from listados.seedwork.dominio.repositorios import Mapeador as RepMap
from listados.modulos.contratos.dominio.entidades import Transaccion
from listados.modulos.contratos.aplicacion.dto import Valor
from .dto import TransaccionDTO

class MapeadorTransaccionDTOJson(AppMap):
    def externo_a_dto(self, externo:dict) -> TransaccionDTO:
        transaccion_dto = TransaccionDTO(
            id='',
            fecha_creacion='',
            fecha_actualizacion='',
            valor=Valor(externo['valor']),
            comprador=externo['comprador'],
            vendedor=externo['vendedor'],
            inquilino=externo['inquilino'],
            arrendatario=externo['arrendatario']
        )
        return transaccion_dto

    def dto_a_externo(self, dto: TransaccionDTO) -> dict:
        return dto.__dict__

class MapeadorTransaccion(RepMap):
    _FORMATO_FECHA = '%Y-%m-%dT%H:%M:%SZ'

    def obtener_tipo(self) -> type:
        print('Este class')
        return Transaccion.__class__

    def entidad_a_dto(self, entidad:Transaccion) -> TransaccionDTO:
        print("entidad_dto: ",entidad)
        _id = str(entidad.id)
        fecha_creacion = entidad.fecha_creacion.strftime(self._FORMATO_FECHA)
        fecha_actualizacion = entidad.fecha_actualizacion.strftime(self._FORMATO_FECHA)
        valor = entidad.valor
        comprador = entidad.comprador
        vendedor = entidad.vendedor
        inquilino = entidad.inquilino
        arrendatario = entidad.arrendatario
        return TransaccionDTO(_id,fecha_creacion,fecha_actualizacion,valor,comprador,vendedor,inquilino,arrendatario)

    def dto_a_entidad(self,dto:TransaccionDTO) -> Transaccion:
        transaccion = Transaccion(
            id=dto.id,
            valor=dto.valor,
            comprador=dto.comprador,
            vendedor=dto.vendedor,
            inquilino=dto.inquilino,
            arrendatario=dto.arrendatario
        )

        return transaccion