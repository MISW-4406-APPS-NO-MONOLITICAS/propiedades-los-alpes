from listados.modulos.arrendamiento.dominio.entidades import Arrendamiento
from listados.modulos.arrendamiento.aplicacion.mapeadores import MapeadorArrendamiento
from listados.seedwork.dominio.repositorios import Mapeador
from listados.seedwork.dominio.fabricas import Fabrica
from dataclasses import dataclass


@dataclass
class FabricaArrendamientos(Fabrica):
    def crear_objeto(self, obj, mapeador: Mapeador | None = None) -> Arrendamiento:
        mapeador = mapeador or MapeadorArrendamiento()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Arrendamiento)
        return result