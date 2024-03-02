from listados.modulos.propiedades.dominio.entidades import Transaccion
from listados.modulos.propiedades.aplicacion.mapeadores import MapeadorTransaccion
from listados.seedwork.dominio.repositorios import Mapeador
from listados.seedwork.dominio.fabricas import Fabrica
from dataclasses import dataclass


@dataclass
class FabricaTransacciones(Fabrica):
    def crear_objeto(self, obj, mapeador: Mapeador | None = None) -> Transaccion:
        mapeador = mapeador or MapeadorTransaccion()
        result = mapeador.dto_a_entidad(obj)
        assert isinstance(result, Transaccion)
        return result
