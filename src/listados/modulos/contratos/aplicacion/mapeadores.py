from datetime import datetime

from listados.seedwork.aplicacion.dto import Mapeador as AppMap
from listados.seedwork.dominio.repositorios import Mapeador as RepMap
from listados.modulos.contratos.dominio.entidades import Transaccion
from .dto import TransaccionDto

class MapeadorTransaccionDTOJson(AppMap):
    def externo_a_dto(self, externo:dict) -> TransaccionDto:
        transaccion_dto = TransaccionDto(
            valor=externo.get('valor'),
            comprador=externo.get('comprador'),
            vendedor=externo.get('vendedor'),
            inquilino=externo.get('inquilino'),
            arrendatario=externo.get('arrendatario')
        )
        return transaccion_dto

    def dto_a_externo(self, dto: TransaccionDto) -> dict:
        return dto.__dict__

