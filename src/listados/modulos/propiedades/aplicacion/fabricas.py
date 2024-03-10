from listados.modulos.propiedades.dominio.entidades import Propiedad
from listados.modulos.propiedades.aplicacion.mapeadores import MapeadorPropiedad
from listados.seedwork.dominio.repositorios import Mapeador
from listados.seedwork.dominio.fabricas import Fabrica
from dataclasses import dataclass

class FabricaPropiedades(Fabrica):
    def crear_objeto(self, dto):
        return Propiedad(
            id=dto.id,
            tipo_construccion=dto.tipo_construccion,
            estado=dto.estado,
            area=dto.area,
            direccion=dto.direccion,
            lote=dto.lote,
            compania=dto.compania,
        )