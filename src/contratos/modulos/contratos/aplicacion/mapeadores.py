from dataclasses import asdict
from contratos.seedwork.dominio.repositorios import Mapeador
from contratos.modulos.contratos.dominio.entidades import Transaccion
from contratos.modulos.contratos.aplicacion.dto import Valor
from .dto import CrearTransaccionDTO


class MapeadorCrearTransaccionDTOJson(Mapeador):
    def externo_a_dto(self, externo: dict) -> CrearTransaccionDTO:
        dto = CrearTransaccionDTO(
            id_propiedad=externo["id_propiedad"],
            valor=Valor(externo["valor"]),
            comprador=externo["comprador"],
            vendedor=externo["vendedor"],
            inquilino=externo["inquilino"],
            arrendatario=externo["arrendatario"],
        )
        return dto

    def dto_a_externo(self, dto: CrearTransaccionDTO) -> dict:
        return asdict(dto)


class MapeadorCrearTransaccion(Mapeador):
    _FORMATO_FECHA = "%Y-%m-%dT%H:%M:%SZ"

    def dto_a_entidad(self, dto: CrearTransaccionDTO) -> Transaccion:
        transaccion = Transaccion(
            id_propiedad=dto.id_propiedad,
            valor=dto.valor,
            comprador=dto.comprador,
            vendedor=dto.vendedor,
            inquilino=dto.inquilino,
            arrendatario=dto.arrendatario,
        )

        return transaccion
