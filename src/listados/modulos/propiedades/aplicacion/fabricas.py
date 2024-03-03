from listados.modulos.propiedades.dominio.entidades import Propiedad
from listados.modulos.propiedades.aplicacion.mapeadores import MapeadorPropiedad
from listados.seedwork.dominio.repositorios import Mapeador
from listados.seedwork.dominio.fabricas import Fabrica
from dataclasses import dataclass


@dataclass
class FabricaPropiedades(Fabrica):
    def crear_objeto(self, obj, mapeador: Mapeador | None = None) -> Propiedad:
        mapeador = mapeador or MapeadorPropiedad()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Propiedad)
        return result
